import json
FILENAME = "shinies.json"

GAME_TO_GEN = {
    "red": 1, "blue": 1, "yellow": 1,
    "gold": 2, "silver": 2, "crystal": 2,
    "ruby": 3, "sapphire": 3, "emerald": 3,
    "fire red": 3, "leaf green": 3,
    "diamond": 4, "pearl": 4, "platinum": 4,
    "heartgold": 4, "soulsilver": 4,
    "black": 5, "white": 5, "black 2": 5, "white 2": 5,
    "x": 6, "y": 6, "omega ruby" : 6, "alpha sapphire" : 6, 
    "sun": 7, "moon": 7, "ultra sun": 7, "ultra moon" : 7, "Let's Go, Pikachu" : 7, "Let's Go, Eevee": 7, 
    "sword": 8, "shield": 8, "Legends: Arceus" : 8, 
    "scarlet": 9, "violet": 9,
    "Legends: Z-A":9, 
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
    next_id = max([s["id"] for s in shinies], default=0) + 1

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
    
def view_stats():
    shinies = load_shinies()

    if not shinies:
        print("No data available for statistics.")
        return

    print("\n=== Shiny Statistics ===")
    print(f"Total Shinies: {len(shinies)}\n")

    # Count by generation
    gen_counts = {}
    for shiny in shinies:
        gen = shiny.get("generation", "Unknown")
        gen_counts[gen] = gen_counts.get(gen, 0) + 1

    print("By Generation:")
    for gen, count in sorted(gen_counts.items(), key=lambda x: str(x[0])):
        print(f"Gen {gen}: {count}")

    print()

    # Count by game
    game_counts = {}
    for shiny in shinies:
        game = shiny.get("game", "Unknown")
        game_counts[game] = game_counts.get(game, 0) + 1

    print("By Game:")
    for game, count in sorted(game_counts.items()):
        print(f"{game}: {count}")

def delete_shiny(shinies):
    if not shinies:
        print("No shinies to delete.")
        return

    view_shinies()  # Show user what's available

    try:
        delete_id = int(input("Enter the ID of the shiny to delete: "))
    except ValueError:
        print("Invalid ID. Must be a number.")
        return

    for shiny in shinies:
        if shiny["id"] == delete_id:
            shinies.remove(shiny)
            print("Shiny deleted!")
            return

    print("No shiny found with that ID.")

    
def main():
    while True:
        shinies = load_shinies()

        print("=== Shiny Pokémon Tracker ===")
        print("1. Add shiny")
        print("2. view shinies")
        print("3. view stats")
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
        elif choice =="4":
            delete_shiny(shinies)
            save_shinies(shinies)
        elif choice == "5":
            print("Goodbye")
            break

        else:
            print("Invalid choice. Try again.")
        

if __name__ == "__main__":
    main()
