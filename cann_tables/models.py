from cann_tables import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    points = db.Column(db.Integer)
    position = db.Column(db.Integer)
    played = db.Column(db.Integer)

    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))

    def __repr__(self):
        return "<Team(id={}, name={}>".format(self.id, self.name)


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_updated = db.Column(db.DateTime)
    max_points = db.Column(db.Integer)
    max_played = db.Column(db.Integer)

    teams = db.relationship("Team", order_by="Team.position", backref=db.backref("league"))

    def __repr__(self):
        return "<League(id={}, name={}>".format(self.id, self.name)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return "<User(username={})>".format(self.username)