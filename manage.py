from flask_script import Manager, Server, Shell, Command
from flask_migrate import MigrateCommand
from flask_frozen import Freezer

from cann_tables import app, db
from cann_tables.models import Team, League
import table_scraper

manager = Manager(app)


def _make_context():
    return {"app": app, "db": db, "Team": Team, "League": League}


class Scrape(Command):
    """Run scraper"""

    def run(self):
        table_scraper.scrape_all()


class Freeze(Command):
    """Create frozen files"""

    def run(self):
        freezer = Freezer(app)
        freezer.freeze()

manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("scrape", Scrape())
manager.add_command("freeze", Freeze())

if __name__ == "__main__":
    manager.run()
