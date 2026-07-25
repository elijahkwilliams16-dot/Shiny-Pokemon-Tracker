from flask import Flask, render_template, request, redirect
from tracker import get_game_sprite, load_shinies, save_shinies, get_pokemon_data, GAME_TO_GEN


app = Flask(__name__)


@app.route("/")
def home():

    shinies = load_shinies()

    for shiny in shinies:

        sprite = get_game_sprite(
            shiny["name"],
            shiny["game"]
        )

        if sprite is None:

            pokemon = get_pokemon_data(
                shiny["name"]
            )

            sprite = pokemon["shiny_sprite"]

        shiny["shiny_sprite"] = sprite

    return render_template(
        "index.html",
        shinies=shinies
    )

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        shinies = load_shinies()


        name = request.form["name"].strip().title()

        game = request.form["game"].strip()

        method = request.form["method"]

        date = request.form["date"]



        # Check Pokémon exists using API

        pokemon_data = get_pokemon_data(name)


        if not pokemon_data["valid"]:

            return "❌ Pokémon not found"


        # Get generation

        generation = GAME_TO_GEN.get(
            game.lower(),
            "Unknown"
        )


        # Create ID

        next_id = max(
            [s.get("id", 0) for s in shinies],
            default=0
        ) + 1



        shiny = {

            "id": next_id,

            "name": name,

            "game": game,

            "method": method,

            "generation": generation,

            "date_caught": date,

            "sprite": pokemon_data["sprite"],

            "shiny_sprite": pokemon_data["shiny_sprite"]

        }



        shinies.append(shiny)

        save_shinies(shinies)


        return redirect("/")



    games = sorted(GAME_TO_GEN.keys())

    return render_template(
        "add.html",
        games=games
)

@app.route("/delete/<int:shiny_id>", methods=["POST"])
def delete(shiny_id):

    shinies = load_shinies()

    shinies = [s for s in shinies if s["id"] != shiny_id]

    save_shinies(shinies)

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)