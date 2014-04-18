from cann_tables import app, db,  models
from flask import render_template


@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html")
