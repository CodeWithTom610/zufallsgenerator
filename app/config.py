class Config:
    SECRET_KEY = "dev"  # Für CSRF Protection usw.
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
