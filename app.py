
from flask import (
    Flask,
    render_template,
    request,
    redirect
)

from config import Config
from extensions import db

from models import (
    Shiny,
    Pokemon,
    Game
)

from tracker import (
    get_pokemon_data,
    get_pokemon_generation,
    get_game_sprite,
    GAME_TO_GEN,
    validate_game
)


# =========================================================
# FLASK SETUP
# =========================================================

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    # -----------------------------------------------------
    # GET FILTER VALUES
    # -----------------------------------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()

    game_filter = request.args.get(
        "game",
        ""
    ).strip()

    generation_filter = request.args.get(
        "generation",
        ""
    ).strip()


    # -----------------------------------------------------
    # START DATABASE QUERY
    # -----------------------------------------------------

    query = Shiny.query


    # -----------------------------------------------------
    # SEARCH BY POKÉMON NAME
    # -----------------------------------------------------

    if search:

        query = query.join(
            Pokemon
        ).filter(
            Pokemon.name.ilike(
                f"%{search.lower()}%"
            )
        )


    # -----------------------------------------------------
    # FILTER BY GAME
    # -----------------------------------------------------

    if game_filter:

        query = query.join(
            Game
        ).filter(
            Game.name == game_filter
        )


    # -----------------------------------------------------
    # FILTER BY GENERATION
    # -----------------------------------------------------

    if generation_filter:

        if not game_filter:

            query = query.join(
                Game
            )

        query = query.filter(
            Game.generation == int(
                generation_filter
            )
        )


    # -----------------------------------------------------
    # GET RESULTS
    # -----------------------------------------------------

    shinies = query.all()


    # -----------------------------------------------------
    # GET FILTER OPTIONS
    # -----------------------------------------------------

    games = Game.query.order_by(
        Game.name
    ).all()


    generations = db.session.query(
        Game.generation
    ).distinct().order_by(
        Game.generation
    ).all()


    generations = [
        generation[0]
        for generation in generations
    ]


    # -----------------------------------------------------
    # RENDER PAGE
    # -----------------------------------------------------

    return render_template(
        "index.html",

        shinies=shinies,

        games=games,

        generations=generations,

        search=search,

        game_filter=game_filter,

        generation_filter=generation_filter
    )


# =========================================================
# ADD SHINY
# =========================================================

@app.route(
    "/add",
    methods=["GET", "POST"]
)
def add():

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        # -------------------------------------------------
        # GET FORM DATA
        # -------------------------------------------------

        name = request.form[
            "name"
        ].strip().title()

        game = request.form[
            "game"
        ].strip()

        method = request.form[
            "method"
        ].strip()

        date = request.form[
            "date"
        ]


        # -------------------------------------------------
        # FIND POKÉMON IN DATABASE
        # -------------------------------------------------

        pokemon = Pokemon.query.filter_by(
            name=name.lower()
        ).first()


        # -------------------------------------------------
        # POKÉMON NOT IN DATABASE
        # -------------------------------------------------

        if pokemon is None:

            pokemon_data = get_pokemon_data(
                name
            )


            # ---------------------------------------------
            # CHECK IF POKÉMON EXISTS
            # ---------------------------------------------

            if not pokemon_data["valid"]:

                return (
                    "❌ Pokémon not found"
                )


            # ---------------------------------------------
            # GET GENERATION
            # ---------------------------------------------

            pokemon_generation = (
                get_pokemon_generation(
                    name
                )
            )


            if pokemon_generation is None:

                return (
                    "❌ Could not determine "
                    "Pokémon generation"
                )


            # ---------------------------------------------
            # CREATE POKÉMON RECORD
            # ---------------------------------------------

            pokemon = Pokemon(

                pokedex_id=
                    pokemon_data["id"],

                name=
                    name.lower(),

                generation=
                    pokemon_generation,

                sprite_url=
                    pokemon_data["sprite"],

                shiny_sprite_url=
                    pokemon_data[
                        "shiny_sprite"
                    ]
            )


            db.session.add(
                pokemon
            )


        # -------------------------------------------------
        # POKÉMON ALREADY EXISTS
        # -------------------------------------------------

        else:

            pokemon_generation = (
                pokemon.generation
            )


            pokemon_data = {

                "valid": True,

                "id":
                    pokemon.pokedex_id,

                "sprite":
                    pokemon.sprite_url,

                "shiny_sprite":
                    pokemon.shiny_sprite_url

            }


        # -------------------------------------------------
        # VALIDATE GAME
        # -------------------------------------------------

        valid, message = validate_game(

            name,

            game,

            pokemon_generation

        )


        if not valid:

            return f"❌ {message}"


        # -------------------------------------------------
        # GET GAME GENERATION
        # -------------------------------------------------

        generation = GAME_TO_GEN.get(
            game.lower()
        )


        if generation is None:

            return (
                "❌ Unknown game"
            )


        # -------------------------------------------------
        # FIND GAME IN DATABASE
        # -------------------------------------------------

        game_record = Game.query.filter_by(
            name=game
        ).first()


        # -------------------------------------------------
        # GAME DOES NOT EXIST
        # -------------------------------------------------

        if game_record is None:

            game_record = Game(

                name=game,

                generation=generation

            )

            db.session.add(
                game_record
            )


        # -------------------------------------------------
        # CHECK FOR DUPLICATE
        # -------------------------------------------------

        duplicate = Shiny.query.filter_by(

            pokemon_id=pokemon.id,

            game_id=game_record.id

        ).first()


        if duplicate:

            return (
                "⚠️ This shiny is "
                "already recorded."
            )


        # -------------------------------------------------
        # GET GAME-SPECIFIC SPRITE
        # -------------------------------------------------

        game_sprite = get_game_sprite(

            name,

            game

        )


        # -------------------------------------------------
        # FALLBACK SPRITE
        # -------------------------------------------------

        if game_sprite is None:

            game_sprite = (
                pokemon_data[
                    "shiny_sprite"
                ]
            )


        # -------------------------------------------------
        # CREATE SHINY
        # -------------------------------------------------

        shiny = Shiny(

            pokemon_id=
                pokemon.id,

            game_id=
                game_record.id,

            method=
                method,

            date_caught=
                date,

            shiny_sprite_url=
                game_sprite

        )


        db.session.add(
            shiny
        )


        # -------------------------------------------------
        # SAVE TO DATABASE
        # -------------------------------------------------

        db.session.commit()


        # -------------------------------------------------
        # RETURN HOME
        # -------------------------------------------------

        return redirect("/")


    # =====================================================
    # GET
    # =====================================================

    games = sorted(
        GAME_TO_GEN.keys()
    )


    return render_template(
        "add.html",

        games=games
    )


# =========================================================
# DELETE SHINY
# =========================================================

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

        db.session.delete(
            shiny
        )

        db.session.commit()


    return redirect("/")


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()


    app.run(
        debug=True
    )
