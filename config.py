import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-this-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://USERNAME:PASSWORD@localhost/DATABASE"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
