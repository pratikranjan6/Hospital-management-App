import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def _truthy(value):
    return str(value).lower() in ("1", "true", "yes", "on")


if load_dotenv:
    backend_dir = Path(__file__).resolve().parent.parent
    dotenv_path = backend_dir / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


class Config:
    DEBUG = _truthy(os.getenv('FLASK_DEBUG', 'True'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):
    DEBUG = _truthy(os.getenv('FLASK_DEBUG', 'True'))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hospitalm.db')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_local_jwt_secret_key')

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', REDIS_URL)


    from celery.schedules import crontab
    CELERY_BEAT_SCHEDULE = {
        'daily-reminder-job': {
            'task': 'application.tasks.send_daily_reminders',
            'schedule': crontab(hour=20,minute=21),
            
        },
        'monthly-report-job': {
            'task': 'application.tasks.send_monthly_reports',
            'schedule': crontab(day_of_month='1', hour=9, minute=0),
        },
    }

    
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', os.getenv('PORT', 25)))
    MAIL_USE_TLS = _truthy(os.getenv('MAIL_USE_TLS', 'False'))
    MAIL_USE_SSL = _truthy(os.getenv('MAIL_USE_SSL', 'False'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@hospitalapp.local')

    GCHAT_WEBHOOK_URL = os.getenv('GCHAT_WEBHOOK_URL', '')
