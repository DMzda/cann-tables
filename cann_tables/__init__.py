from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object("cann_tables.config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

csrf = CsrfProtect(app)

from cann_tables import views, models
