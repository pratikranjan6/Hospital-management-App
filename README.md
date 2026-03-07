# Mad2-Hospital-management-App
Hospitals need efficient systems to manage patients, doctors, appointments, and treatments. Currently, many hospitals use manual registers or disconnected software, which makes it difficult to manage records, avoid scheduling conflicts, and track patient history.

## Background Jobs & Async Tasks

The backend now leverages Redis and Celery to perform scheduled jobs and long running operations:

* **Daily reminders** – every morning the system checks for appointments on the current day and sends a reminder email to the patient.
* **Monthly reports** – on the first of each month a summary of the previous month's appointments (diagnosis/testing/prescriptions) is generated and emailed to each doctor.
* **Export history** – patients can trigger a CSV export of their treatment details from their dashboard; the request is processed asynchronously and the resulting file is emailed.

Redis is also used as a simple cache for expensive GET endpoints (doctors/patients lists).

If a `GCHAT_WEBHOOK_URL` is configured the daily reminders will be posted to that
webhook instead of being emailed – this makes it easy to push reminders to a
Google Chat room.

### Setup Notes

1. Install dependencies: `pip install flask celery redis requests` (plus any existing requirements).
2. Make sure a Redis server is running (`redis-server`).
3. Start the flask app as usual (`python app.py`).
4. In a separate shell start the celery worker with beat enabled:
   ```bash
   cd backend
   python celery_worker.py
   ```
5. Configure SMTP settings in `application/config.py` or via environment variables if you want real emails.

The frontend includes an "Export CSV" button on the patient dashboard that calls the new `/api/patient/export_history` endpoint.
