import json
import requests
import os
FILENAME = os.path.join(
    os.path.dirname(__file__),
    "shinies.json"
)

GAME_TO_GEN = {
    "red": 1, "blue": 1, "yellow": 1,
    "gold": 2, "silver": 2, "crystal": 2,
    "ruby": 3, "sapphire": 3, "emerald": 3,
    "fire red": 3, "leaf green": 3,
    "diamond": 4, "pearl": 4, "platinum": 4,
    "heartgold": 4, "soulsilver": 4,
    "black": 5, "white": 5, "black 2": 5, "white 2": 5,
    "x": 6, "y": 6,
    "omega ruby": 6, "alpha sapphire": 6,
    "sun": 7, "moon": 7,
    "ultra sun": 7, "ultra moon": 7,
    "let's go, pikachu": 7,
    "let's go, eevee": 7,
    "sword": 8, "shield": 8,
    "legends: arceus": 8,
    "scarlet": 9, "violet": 9,
    "legends: z-a": 9,
}

GAME_TO_VERSION = {

    # ==========================
    # Generation I
    # ==========================
    "red": ("generation-i", "red-blue"),
    "blue": ("generation-i", "red-blue"),
    "yellow": ("generation-i", "yellow"),

    # ==========================
    # Generation II
    # ==========================
    "gold": ("generation-ii", "gold"),
    "silver": ("generation-ii", "silver"),
    "crystal": ("generation-ii", "crystal"),

    # ==========================
    # Generation III
    # ==========================
    "ruby": ("generation-iii", "ruby-sapphire"),
    "sapphire": ("generation-iii", "ruby-sapphire"),
    "emerald": ("generation-iii", "emerald"),
    "fire red": ("generation-iii", "firered-leafgreen"),
    "leaf green": ("generation-iii", "firered-leafgreen"),

    # ==========================
    # Generation IV
    # ==========================
    "diamond": ("generation-iv", "diamond-pearl"),
    "pearl": ("generation-iv", "diamond-pearl"),
    "platinum": ("generation-iv", "platinum"),
    "heartgold": ("generation-iv", "heartgold-soulsilver"),
    "soulsilver": ("generation-iv", "heartgold-soulsilver"),

    # ==========================
    # Generation V
    # ==========================
    "black": ("generation-v", "black-white"),
    "white": ("generation-v", "black-white"),
    "black 2": ("generation-v", "black-2-white-2"),
    "white 2": ("generation-v", "black-2-white-2"),

    # ==========================
    # Generation VI
    # ==========================
    "x": ("generation-vi", "x-y"),
    "y": ("generation-vi", "x-y"),
    "omega ruby": ("generation-vi", "omegaruby-alphasapphire"),
    "alpha sapphire": ("generation-vi", "omegaruby-alphasapphire"),

    # ==========================
    # Generation VII
    # ==========================
    "sun": ("generation-vii", "ultra-sun-ultra-moon"),
    "moon": ("generation-vii", "ultra-sun-ultra-moon"),
    "ultra sun": ("generation-vii", "ultra-sun-ultra-moon"),
    "ultra moon": ("generation-vii", "ultra-sun-ultra-moon"),
    "let's go, pikachu": ("generation-vii", "icons"),
    "let's go, eevee": ("generation-vii", "icons"),

    # ==========================
    # Generation VIII
    # ==========================
    "sword": ("generation-viii", "icons"),
    "shield": ("generation-viii", "icons"),
    "legends: arceus": ("generation-viii", "icons"),

    # ==========================
    # Generation IX
    # ==========================
    "scarlet": ("generation-ix", "scarlet-violet"),
    "violet": ("generation-ix", "scarlet-violet"),
    "legends: z-a": ("generation-ix", "scarlet-violet")
}

def load_shinies():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_shinies(shinies):
    with open(FILENAME, "w") as file:
        json.dump(shinies, file, indent=4)




# ==========================
# POKEAPI FUNCTIONS
# ==========================
def get_pokemon_generation(name):

    pokemon_name = name.lower().strip()

    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        # Make sure the API actually returned generation information
        if "generation" not in data:
            return None

        generation_name = data["generation"]["name"]

        generation_map = {
            "generation-i": 1,
            "generation-ii": 2,
            "generation-iii": 3,
            "generation-iv": 4,
            "generation-v": 5,
            "generation-vi": 6,
            "generation-vii": 7,
            "generation-viii": 8,
            "generation-ix": 9
        }

        return generation_map.get(generation_name)

    except requests.exceptions.RequestException:

        return None  



def validate_game(name, game):

    pokemon_generation = get_pokemon_generation(name)

    if pokemon_generation is None:

        return (
            False,
            "Could not determine the Pokémon's generation. Please try again."
        )

    game_generation = GAME_TO_GEN.get(
        game.lower()
    )

    if game_generation is None:

        return (
            False,
            "Unknown game."
        )

    if pokemon_generation > game_generation:

        return (
            False,
            f"{name} was introduced in Generation {pokemon_generation}."
        )

    return True, ""

def get_pokemon_data(name):
    pokemon_name = name.lower().strip()

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    try:
        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            official_art = data["sprites"]["other"]["official-artwork"]

            shiny_sprite = official_art["front_shiny"]

            # Backup if official shiny artwork doesn't exist
            if shiny_sprite is None:
                shiny_sprite = data["sprites"]["front_shiny"]


            normal_sprite = official_art["front_default"]

            if normal_sprite is None:
                normal_sprite = data["sprites"]["front_default"]


            return {
                "valid": True,
                "id": data["id"],
                "sprite": normal_sprite,
                "shiny_sprite": shiny_sprite
            }


        else:
            return {
                "valid": False
            }


    except requests.exceptions.RequestException:
        print("Could not connect to PokéAPI.")

        return {
            "valid": False
        }

def get_game_sprite(name, game):

    pokemon_name = name.lower().strip()

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        if game.lower() not in GAME_TO_VERSION:
            return None

        generation, version = GAME_TO_VERSION[game.lower()]

        sprite = (
            data["sprites"]
                ["versions"]
                [generation]
                [version]
                .get("front_shiny")
        )

        return sprite

    except (KeyError, requests.exceptions.RequestException):
        return None

# ==========================
# ADD SHINY
# ==========================

def add_shiny(shinies):

    next_id = max([s.get("id", 0) for s in shinies], default=0) + 1
    name = input("Pokémon name: ").strip().title()


    # Check Pokémon exists
    pokemon_data = get_pokemon_data(name)

    if not pokemon_data["valid"]:
        print("Pokémon not found. Check spelling.")
        return


    game = input("Game caught in: ").strip()
    game_key = game.lower()
    generation = GAME_TO_GEN.get(game_key, "Unknown")
    game_sprite = get_game_sprite(name, game)

    if game_sprite is None:
        game_sprite = pokemon_data["shiny_sprite"]


    if generation == "Unknown":
        print("Game not recognized — generation set to Unknown.")


    method = input("Method: ")
    date = input("Date caught (YYYY-MM-DD): ")


    # Duplicate check

    for s in shinies:

        if (
            s.get("name", "").lower() == name.lower()
            and
            s.get("game", "").lower() == game.lower()
        ):

            print("⚠️ This shiny is already recorded.")
            return

    valid, message = validate_game(name, game)
    if not valid:
        print(message)
        return

    shiny = {
    "id": next_id,
    "name": name,
    "game": game,
    "method": method,
    "generation": generation,
    "date_caught": date
    }


    shinies.append(shiny)
    print("✨ Shiny added!")



# ==========================
# VIEW SHINIES
# ==========================

def view_shinies():

    shinies = load_shinies()

    if not shinies:

        print("No Shiny Pokémon recorded yet.")
        return



    for shiny in shinies:

        print("-" * 30)
        print(f"ID: {shiny.get('id', 'Unknown')}")
        print(f"Pokémon: {shiny.get('name', 'Unknown')}")
        print(f"Game: {shiny.get('game', 'Unknown')}")
        print(f"Generation: {shiny.get('generation', 'Unknown')}")
        print(f"Method: {shiny.get('method', 'Unknown')}")
        print(f"Date: {shiny.get('date_caught', 'Unknown')}")
        print("-" * 30)



# ==========================
# STATS
# ==========================

def view_stats():

    shinies = load_shinies()

    if not shinies:

        print("No data available for statistics.")
        return


    print("\n=== Shiny Statistics ===")
    print(f"Total Shinies: {len(shinies)}\n")


    gen_counts = {}


    for shiny in shinies:
        gen = shiny.get("generation", "Unknown")
        gen_counts[gen] = gen_counts.get(gen, 0) + 1



    print("By Generation:")
    for gen, count in sorted(gen_counts.items(), key=lambda x: str(x[0])):
        print(f"Gen {gen}: {count}")



    game_counts = {}


    for shiny in shinies:
        game = shiny.get("game", "Unknown")
        game_counts[game] = game_counts.get(game, 0) + 1



    print("\nBy Game:")

    for game, count in sorted(game_counts.items()):
        print(f"{game}: {count}")




# ==========================
# DELETE
# ==========================

def delete_shiny(shinies):

    if not shinies:
        print("No shinies to delete.")
        return



    view_shinies()

    try:
        delete_id = int(input("Enter ID to delete: "))

    except ValueError:
        print("Invalid ID.")
        return



    for shiny in shinies:
        if shiny.get("id") == delete_id:
            shinies.remove(shiny)

            print("✨ Shiny deleted!")
            return



    print("No shiny found with that ID.")




# ==========================
# MAIN MENU
# ==========================

def main():

    while True:

        shinies = load_shinies()

        print("\n=== Shiny Pokémon Tracker ===")
        print("1. Add shiny")
        print("2. View shinies")
        print("3. View stats")
        print("4. Delete shiny")
        print("5. Exit")


        choice = input("Choose an option: ")

        if choice == "1":
            add_shiny(shinies)
            save_shinies(shinies)

        elif choice == "2":
            view_shinies()

        elif choice == "3":
            view_stats()

        elif choice == "4":

            delete_shiny(shinies)
            save_shinies(shinies)



        elif choice == "5":
            print("Goodbye!")
            break



        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()