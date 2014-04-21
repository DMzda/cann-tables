from cann_tables import app, models, login_manager, forms
from flask import render_template, flash, redirect, g, url_for
from flask_login import login_required

import datetime


@app.route("/")
@app.route("/index/")
def index():
    leagues = models.League.query.order_by(models.League.id).all()
    data = {}
    for league in leagues:
        league.last_updated = datetime.datetime.strftime(league.last_updated, "%a %d/%m/%Y %I:%M %p GMT")
        max_points = league.teams[0].points
        min_points = league.teams[-1].points

        data[league] = {point: [] for point in range(max_points, min_points - 1, -1)}

        for team in league.teams:
            data[league][team.points].append(team)

    #leagues is used for ordering
    return render_template("index.html", leagues=leagues, data=data)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if g.user and g.user.is_authenticated():
        return redirect(url_for("admin"))

    form = forms.LoginForm()

    if form.validate_on_submit():
        flash("Login: Username:{}, Remember me:{}".format(form.username.data, form.remember_me.data), category="info")
        #return redirect("/admin/")

    return render_template("login.html", form=form)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    pass


@login_required
@app.route("/admin/", methods=["GET", "POST"])
def admin():
    return "a"