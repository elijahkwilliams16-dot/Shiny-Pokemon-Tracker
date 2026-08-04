from extensions import db


class Shiny(db.Model):

    __tablename__ = "shinies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    game = db.Column(
        db.String(100),
        nullable=False
    )

    generation = db.Column(
        db.Integer,
        nullable=False
    )

    method = db.Column(
        db.String(100),
        nullable=False
    )

    date_caught = db.Column(
        db.String(20),
        nullable=False
    )