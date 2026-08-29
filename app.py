from flask import Flask, render_template, request, redirect

from config import Config
from extensions import db

from models import Shiny, Pokemon, Game

from tracker import (
    get_pokemon_data,
    get_pokemon_generation,
    get_game_sprite,
    GAME_TO_GEN,
    validate_game
    
)


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    shinies = Shiny.query.all()

    return render_template(
        "index.html",
        shinies=shinies
    )


# ==========================
# ADD SHINY
# ==========================

@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"].strip().title()

        game = request.form["game"].strip()

        method = request.form["method"].strip()

        date = request.form["date"]


        # Check Pokémon using PokéAPI

        pokemon_data = get_pokemon_data(name)

        if not pokemon_data["valid"]:

            return "❌ Pokémon not found"


        # Check if Pokémon can exist in this game

        valid, message = validate_game(
            name,
            game
        )

        if not valid:

            return f"❌ {message}"


        # Get game generation

        generation = GAME_TO_GEN.get(
            game.lower()
        )

        if generation is None:

            return "❌ Unknown game"


        # ==========================
        # FIND POKÉMON
        # ==========================

        pokemon = Pokemon.query.filter_by(
            name=name.lower()
        ).first()


        # Create Pokémon if it doesn't exist

        if pokemon is None:

            pokemon = Pokemon(

                pokedex_id=pokemon_data["id"],

                name=name.lower(),

                generation=get_pokemon_generation(name),

                sprite_url=pokemon_data["sprite"],

                shiny_sprite_url=pokemon_data["shiny_sprite"]

            )

            db.session.add(pokemon)


        # ==========================
        # FIND GAME
        # ==========================

        game_record = Game.query.filter_by(
            name=game
        ).first()


        # Create game if it doesn't exist

        if game_record is None:

            game_record = Game(

                name=game,

                generation=generation

            )

            db.session.add(game_record)


        # ==========================
        # DUPLICATE CHECK
        # ==========================

        duplicate = Shiny.query.filter_by(

            pokemon=pokemon,

            game=game_record

        ).first()


        if duplicate:

            return "⚠️ This shiny is already recorded."


        # ==========================
        # CREATE SHINY
        # ==========================

        shiny = Shiny(

            pokemon=pokemon,

            game=game_record,

            method=method,

            date_caught=date

        )

        db.session.add(shiny)

        db.session.commit()


        return redirect("/")


    # GET request

    games = sorted(GAME_TO_GEN.keys())


    return render_template(
        "add.html",
        games=games
    )


# ==========================
# DELETE SHINY
# ==========================

@app.route(
    "/delete/<int:shiny_id>",
    methods=["POST"]
)
def delete(shiny_id):

    shiny = db.session.get(
        Shiny,
        shiny_id
    )


    if shiny:

        db.session.delete(shiny)

        db.session.commit()


    return redirect("/")


# ==========================
# START APP
# ==========================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()


    app.run(debug=True)