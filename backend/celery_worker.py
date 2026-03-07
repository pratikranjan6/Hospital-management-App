from app import app
from application.tasks import init_celery

celery = init_celery(app)

if __name__ == '__main__':
    celery.worker_main(['worker', '--loglevel=info', '--beat'])
