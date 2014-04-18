from cann_tables import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    points = db.Column(db.Integer)
    position = db.Column(db.Integer)
    played = db.Column(db.Integer)

    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    league = db.relationship("League", backref=db.backref("teams"))

    def __repr__(self):
        return "<Team(id={}, name={}>".format(self.id, self.name)


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_updated = db.Column(db.DateTime)
    max_points = db.Column(db.Integer)

    def __repr__(self):
        return "<League(id={}, name={}>".format(self.id, self.name)
