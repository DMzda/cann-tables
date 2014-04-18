from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("cann_tables.config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from cann_tables import views, models
