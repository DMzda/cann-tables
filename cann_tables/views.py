from cann_tables import app, models
from flask import render_template

import datetime


@app.route("/")
@app.route("/index/")
def index():
    leagues = models.League.query.all()
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
