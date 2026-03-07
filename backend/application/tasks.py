import csv
import io
import os
from datetime import datetime, date, timedelta
from flask import render_template_string
from celery import Celery
from .database import db
from .models import Appointment, Patient, Doctor
from .cache import redis_client
import smtplib
from email.message import EmailMessage
import importlib

# helper to lazily create/get the Flask app when tasks run in a separate process
_flask_app = None
def get_flask_app():
    global _flask_app
    if _flask_app is not None:
        return _flask_app
    try:
        # ensure backend folder is on sys.path so top-level `app` module is importable
        import sys
        from pathlib import Path
        backend_dir = Path(__file__).resolve().parents[1]
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        # import top-level app module and call create_app()
        app_mod = importlib.import_module('app')
        if hasattr(app_mod, 'create_app'):
            _flask_app = app_mod.create_app()
            return _flask_app
    except Exception as e:
        import traceback
        traceback.print_exc()
        print('get_flask_app import/create_app failed:', e)
    return None


# create celery object early so decorators work; config will be updated later
candidate_broker = os.getenv('CELERY_BROKER_URL', None)
if candidate_broker:
    celery = Celery('application.tasks', broker=candidate_broker)
else:
    celery = Celery('application.tasks')


def init_celery(flask_app):
    """Configure celery with the Flask app's settings and wrap tasks in the
    application context.
    """
    celery.conf.update(flask_app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# ---------- helpers -------------------------------------------------------------

def send_email(to_address: str, subject: str, body: str, attachment: tuple = None):
    """Simple SMTP helper that sends an email using configuration defined in
    app.config.  If MAIL_SERVER is 'localhost' it will just print the message
    instead of raising an error, which is convenient for development.
    """
    msg = EmailMessage()
    flask_app = get_flask_app()
    cfg = flask_app.config if flask_app else {}
    msg['From'] = cfg.get('MAIL_DEFAULT_SENDER', 'noreply@localhost')
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body, subtype='html')

    if attachment:
        filename, data, mimetype = attachment
        msg.add_attachment(data, maintype=mimetype.split('/')[0], subtype=mimetype.split('/')[1], filename=filename)

    try:
        mail_server = cfg.get('MAIL_SERVER', 'localhost')
        mail_port = cfg.get('MAIL_PORT', 25)
        mail_use_tls = cfg.get('MAIL_USE_TLS')
        usr = cfg.get('MAIL_USERNAME')
        pwd = cfg.get('MAIL_PASSWORD')
        with smtplib.SMTP(mail_server, mail_port) as server:
            if mail_use_tls:
                server.starttls()
            if usr and pwd:
                server.login(usr, pwd)
            server.send_message(msg)
    except Exception as e:
        if flask_app and hasattr(flask_app, 'logger'):
            flask_app.logger.exception('Failed to send email to %s', to_address)
        else:
            print('Failed to send email to', to_address, e)


def send_chat_message(webhook: str, message: str):
    """Post a simple text card to a Google Chat webhook. If the request fails
    it is logged but otherwise ignored.
    """
    try:
        import requests
        payload = {"text": message}
        requests.post(webhook, json=payload, timeout=5)
    except Exception as e:
        flask_app = get_flask_app()
        if flask_app and hasattr(flask_app, 'logger'):
            flask_app.logger.exception('Failed to send chat message to %s', webhook)
        else:
            print('Failed to send chat message to', webhook, e)


# ---------- periodic / scheduled tasks -----------------------------------------

@celery.task(name='application.tasks.send_daily_reminders')
def send_daily_reminders():
    """Check for any appointments happening today and alert the patient via
    email.  Runs every morning according to the beat schedule configured in
    config.py.
    """
    flask_app = get_flask_app()
    if not flask_app:
        print('No Flask app available for send_daily_reminders')
        return
    with flask_app.app_context():
        today = date.today()
        # query by date portion only
        appts = Appointment.query.filter(db.func.date(Appointment.appointment_date) == today).all()
        for appt in appts:
            pat = appt.patient
            if not pat:
                continue
            user = pat.user
            if not user:
                continue
            when = appt.appointment_date.strftime('%Y-%m-%d %H:%M')
            subject = 'Appointment Reminder'
            body = f"<p>Dear {pat.name},</p>\
                    <p>This is a reminder that you have an appointment with Dr. {appt.doctor.name}\
                    on <strong>{when}</strong>.</p>\
                    <p>Please arrive a few minutes early.</p>"

            # preference order: chat webhook -> email
            webhook = flask_app.config.get('GCHAT_WEBHOOK_URL')
            if webhook:
                send_chat_message(webhook, f"Reminder for {pat.name}: appointment at {when}")
            else:
                send_email(user.username, subject, body)


@celery.task(name='application.tasks.send_monthly_reports')
def send_monthly_reports():
    """Generate and send an HTML activity report to each doctor for the
    previous calendar month.  Triggered on the first day of every month.
    """
    flask_app = get_flask_app()
    if not flask_app:
        print('No Flask app available for send_monthly_reports')
        return
    with flask_app.app_context():
        now = datetime.now()
        first_of_this = now.replace(day=1)
        last_month_end = first_of_this - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        doctors = Doctor.query.all()
        for doc in doctors:
            appts = Appointment.query.filter(
                Appointment.doctor_id == doc.id,
                Appointment.appointment_date >= last_month_start,
                Appointment.appointment_date <= last_month_end
            ).all()
            # build HTML report
            rows = []
            for a in appts:
                rows.append(f"<tr><td>{a.patient.name if a.patient else 'N/A'}</td>"
                            f"<td>{a.appointment_date.strftime('%Y-%m-%d')}</td>"
                            f"<td>{a.diagnosis}</td>"
                            f"<td>{a.prescription}</td></tr>")
            report_html = f"""
            <h2>Activity report for {last_month_start.strftime('%B %Y')}</h2>
            <p>Doctor: {doc.name}</p>
            <table border='1' cellpadding='4' cellspacing='0'>
                <thead><tr><th>Patient</th><th>Date</th><th>Diagnosis</th><th>Treatment</th></tr></thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
            """
            # send to doctor's username which we expect to be an email
            if doc.username:
                send_email(doc.username, f"Monthly activity report - {last_month_start.strftime('%B %Y')}", report_html)


# ---------- user‑triggered asynchronous jobs -----------------------------------

@celery.task(name='application.tasks.export_patient_history')
def export_patient_history(user_id: int):
    """Produce a CSV file containing all treatment history for the patient
    associated with *user_id*.  Once completed an email is sent to the user
    with the CSV attached.
    """
    flask_app = get_flask_app()
    if not flask_app:
        print('No Flask app available for export_patient_history')
        return
    with flask_app.app_context():
        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            flask_app.logger.warning('export_patient_history called for missing user %s', user_id)
            return

        appointments = patient.appointments  # includes diagnosis/prescription fields

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'user_id', 'username', 'doctor', 'appointment_date',
            'diagnosis', 'prescription', 'next_visit'
        ])
        for a in appointments:
            writer.writerow([
                patient.user_id,
                patient.user.username,
                a.doctor.name if a.doctor else '',
                a.appointment_date.strftime('%Y-%m-%d %H:%M'),
                a.diagnosis or '',
                a.prescription or '',
                ''  # next visit not tracked on appointment model
            ])

        csv_data = output.getvalue().encode('utf-8')
        subject = 'Your treatment history export'
        body = '<p>Please find attached the CSV file containing your treatment details.</p>'
        send_email(patient.user.username, subject, body,
                   attachment=('history.csv', csv_data, 'text/csv'))

        # optionally cache a flag to show job completed if needed
        try:
            redis_client.setex(f"export_done:{user_id}", 3600, '1')
        except Exception:
            # if redis isn't available just ignore
            pass
