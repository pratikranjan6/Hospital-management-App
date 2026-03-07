from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User, Doctor, Patient, Department, Appointment, Availability
from application.security import jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)

    from application.tasks import init_celery
    init_celery(app)


    CORS(app,
         supports_credentials=True,
         resources={r"/api/*": {"origins": ["http://localhost:5173"]}},
         allow_headers=["Content-Type", "Authorization"],
         expose_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="Pratik@13").first():
            admin_user = User(
                username="Pratik@13",
                password="PRB1306",
                full_name="Pratik Ranjan Bishwal",
                address="Sohela",
                admin=True
            )
            db.session.add(admin_user)
            db.session.commit()

        from datetime import date, timedelta
        def seed_availability():
            today = date.today()
            doctors = Doctor.query.all()
            for doc in doctors:
                for i in range(7):
                    d = today + timedelta(days=i)
                    exists = Availability.query.filter_by(doctor_id=doc.id, date=d).first()
                    if not exists:
                        db.session.add(Availability(doctor_id=doc.id, date=d))
            db.session.commit()

        seed_availability()

        from application import routes
    return app

app = create_app()

if __name__ == '__main__':
    app.run()