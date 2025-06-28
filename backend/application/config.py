class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///ecardDb.sqlite3"
    JWT_SECRET_KEY = "this-is-a-secret-key"
    # SECURITY_PASSWORD_HASH = "bcrypt"
    