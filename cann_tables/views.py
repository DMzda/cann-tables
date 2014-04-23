from cann_tables import app, login_manager, forms
from cann_tables.models import League, User
from cann_tables.utils import passwd_context
from cann_tables.scraper import scrape_all

from flask import render_template, flash, redirect, g, url_for, request, make_response
from flask_login import login_required, current_user, login_user, logout_user

import datetime


@app.route("/")
@app.route("/index/", methods=["GET", "POST"])
def index():
    leagues = None
    wanted_leagues = None
    all_leagues = League.query.order_by(League.id).all()

    if request.method == "POST" or "leagues" in request.cookies:
        if request.form:
            wanted_leagues = request.form.getlist("league")
        else:
            wanted_leagues = request.cookies.get("leagues").split(",")

        if request.form.get("reset"):
            leagues = all_leagues
            wanted_leagues = None
        elif wanted_leagues:
            leagues = League.query.filter(League.id.in_(wanted_leagues)).order_by(League.id).all()
        else:
            # A form could be submitted empty
            flash("Please select your leagues", category="warning")

    if not leagues:
        leagues = all_leagues

    data = {}
    for league in leagues:
        league.last_updated = datetime.datetime.strftime(league.last_updated, "%a %d/%m/%Y %I:%M %p GMT")
        max_points = league.teams[0].points
        min_points = league.teams[-1].points

        data[league] = {point: [] for point in range(max_points, min_points - 1, -1)}

        for team in league.teams:
            data[league][team.points].append(team)

    #leagues is used for ordering
    response = make_response(render_template("index.html", all_leagues=all_leagues, leagues=leagues, data=data))
    if wanted_leagues:
        #Update/create cookie holding wanted_leagues
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=60)
        response.set_cookie("leagues", ",".join(wanted_leagues), expires=expires)
    elif "leagues" in request.cookies:
        #Delete cookie
        response.set_cookie("leagues", "", expires=0)
    return response


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route("/login/", methods=["GET", "POST"])
def login():
    if g.user and g.user.is_authenticated():
        return redirect(url_for("admin"))

    form = forms.LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user:
            if passwd_context.verify(form.password.data, user.password):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("admin"))

        flash("Invalid username or password", category="danger")

    return render_template("login.html", form=form)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin/", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        scrape_all()
        flash("All tables updated", category="info")

    return render_template("admin.html")