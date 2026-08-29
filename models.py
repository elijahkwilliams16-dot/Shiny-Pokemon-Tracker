from extensions import db


class Pokemon(db.Model):

    __tablename__ = "pokemon"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pokedex_id = db.Column(
        db.Integer,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    generation = db.Column(
        db.Integer,
        nullable=False
    )

    sprite_url = db.Column(
        db.String(500)
    )

    shiny_sprite_url = db.Column(
        db.String(500)
    )


class Game(db.Model):

    __tablename__ = "games"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    generation = db.Column(
        db.Integer,
        nullable=False
    )


class Shiny(db.Model):

    __tablename__ = "shinies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    pokemon_id = db.Column(
        db.Integer,
        db.ForeignKey("pokemon.id"),
        nullable=False
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.id"),
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

    # Sprite specifically for this shiny/game combination
    shiny_sprite_url = db.Column(
        db.String(500)
    )

    pokemon = db.relationship(
        "Pokemon",
        backref="shinies"
    )

    game = db.relationship(
        "Game",
        backref="shinies"
    )