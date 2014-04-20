import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if os.environ.get("CANN_ENV") == "prod":
    #Postgresql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') + "?client_encoding=utf8"
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(APP_ROOT, "cann.db")
