from flask_script import Manager, Server, Shell
from flask_migrate import MigrateCommand

from cann_tables import app, db, utils, scraper
from cann_tables.models import Team, League, User


manager = Manager(app)


def _make_context():
    return {"app": app, "db": db, "Team": Team, "League": League, "User": User}


@manager.command
def scrape():
    """Run scraper"""
    scraper.scrape_all()


@manager.command
def add_user():
    """Add a user to the database"""
    utils.add_user()


manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == "__main__":
    manager.run()
