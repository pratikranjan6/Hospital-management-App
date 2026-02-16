class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospitalm.db'
    JWT_SECRET_KEY = 'your_local_jwt_secret_key'