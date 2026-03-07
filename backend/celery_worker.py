from app import app
from application.tasks import init_celery

# ensure flask app context is created before celery
celery = init_celery(app)

if __name__ == '__main__':
    # keep the worker process running when invoked directly
    celery.worker_main(['worker', '--loglevel=info', '--beat'])
