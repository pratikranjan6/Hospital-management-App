from celery import Celery


def make_celery(app):
    """Initialize a Celery object that works with the Flask app context.

    This is the standard pattern from the Flask documentation. Tasks defined
    using this object will automatically run inside an application context,
    giving them access to the database and other Flask extensions.
    """
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
