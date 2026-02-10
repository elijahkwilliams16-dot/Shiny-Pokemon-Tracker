import json
FILENAME = "shinies.json"

GAME_TO_GEN = {
    "red": 1, "blue": 1, "yellow": 1,
    "gold": 2, "silver": 2, "crystal": 2,
    "ruby": 3, "sapphire": 3, "emerald": 3,
    "firered": 3, "leafgreen": 3,
    "diamond": 4, "pearl": 4, "platinum": 4,
    "heartgold": 4, "soulsilver": 4,
    "black": 5, "white": 5,
    "x": 6, "y": 6,
    "sun": 7, "moon": 7,
    "sword": 8, "shield": 8,
    "scarlet": 9, "violet": 9,
    "za":9, 
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

def add_shiny(shinies):
    next_id = len(shinies) + 1

    # Normalize name
    name = input("Pokémon name: ").strip().title()

    # Normalize game + derive generation
    game = input("Game caught in: ").strip()
    game_key = game.lower()
    generation = GAME_TO_GEN.get(game_key, "Unknown")

    if generation == "Unknown":
        print("⚠️ Game not recognized — generation set to Unknown.")

    method = input("Method: ")
    date = input("Date caught (YYYY-MM-DD): ")

    # Duplicate check (must happen BEFORE append)
    for s in shinies:
        if s["name"].lower() == name.lower() and s["game"].lower() == game.lower():
            print("⚠️ This shiny is already recorded.")
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


def view_shinies():
    shinies = load_shinies()

    if not shinies:
        print("No Shiny Pokémon recorded yet.")
        return

    for shiny in shinies:
        print("-" * 30)
        print(f"ID: {shiny['id']}")
        print(f"Pokémon: {shiny['name']}")
        print(f"Game: {shiny['game']}")
        print(f"Generation: {shiny['generation']}")
        print(f"Method: {shiny['method']}")
        print(f"Date: {shiny['date_caught']}")
        print("-" * 30)


    
def main():
    shinies = load_shinies()

    print("=== Shiny Pokémon Tracker ===")
    print("1. Add shiny")
    print("2. view shinies")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_shiny(shinies)
        save_shinies(shinies)
    elif choice == "2":
        view_shinies()


if __name__ == "__main__":
    main()
