import requests
from lxml import html
from cssselect import HTMLTranslator
import datetime
import json

from cann_tables import db
from cann_tables.models import Team, League


def choose_tables():
    """Use this to create your own list of leagues.
    You way want to edit wanted.json manually to correct names"""
    url = "http://www.bbc.co.uk/sport/football/tables"
    page = requests.get(url)
    tree = html.fromstring(page.text)

    wanted = {}
    sel = HTMLTranslator().css_to_xpath(".stats-body>div option[value^=competition]")
    for league in tree.xpath(sel):
        print(league.text, league.attrib["value"])
        answer = input("y/n: ")
        if answer.lower() == "y":
            l_id = league.attrib["value"].split("-")[-1]
            name = league.text.strip()
            wanted[l_id] = name

    with open("wanted.json", "w") as f:
        json.dump(wanted, f, indent=4)


def add_from_json():
    """Adds leagues to the database from wanted.json"""
    with open("wanted.json", "r") as f:
        wanted = json.load(f)

    for l_id, name in wanted.items():
        l = League(id=int(l_id), name=name)
        db.session.add(l)

    db.session.commit()


def scrape_table(league):
    url = "http://www.bbc.co.uk/sport/football/tables/partial/{}".format(league.id)
    page = requests.get(url)
    tree = html.fromstring(page.text)

    sel = {"position": '//*/span[@class="position-number"]/text()',
           "name": '//*/td[@class="team-name"]//text()',
           "points": '//*/td[@class="points"]/text()',
           "played": '//*/td[@class="played"]/text()',
           }

    results = {}

    for item, selector in sel.items():
        values = tree.xpath(selector)
        results[item] = values

    max_points = int(max(results["played"])) * 3
    now = datetime.datetime.utcnow()

    league.last_updated = now
    league.max_points = max_points


    max_played = 0

    for index, _ in enumerate(results["position"]):
        name = results["name"][index]
        points = int(results["points"][index])
        position = int(results["position"][index])
        played = int(results["played"][index])

        if played > max_played:
            max_played = played

        t = Team.query.filter(Team.league_id == league.id).filter(Team.name == name).first()
        if t:
            t.points = points
            t.position = position
            t.played = played
        else:
            t = Team(name=name, points=points, position=position, played=played, league=league)

        db.session.add(t)

    league.max_played = max_played
    db.session.add(league)
    db.session.commit()
    print("{} completed".format(league.name))


def scrape_all():
    leagues = League.query.all()

    for league in leagues:
        scrape_table(league)


def setup():
    """Run first"""
    choose_tables()
    add_from_json()


if __name__ == "__main__":
    scrape_all()