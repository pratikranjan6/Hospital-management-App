from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User, Doctor, Patient, Appointment,Department
from application.security import jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    # Allow CORS from the Vite dev server and enable credentials for cookie/session flows.
    # Adjust origin if your frontend runs on a different host/port.
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173"}})
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
        from application import routes
    return app

app = create_app()

if __name__ == '__main__':
    app.run()