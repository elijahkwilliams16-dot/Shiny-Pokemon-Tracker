import requests
import json


url = "https://pokeapi.co/api/v2/pokemon-species?limit=2000"

response = requests.get(url)

response.raise_for_status()

data = response.json()


pokemon_names = []

for pokemon in data["results"]:

    name = pokemon["name"].replace("-", " ").title()

    pokemon_names.append(name)


pokemon_names.sort()


with open("static/pokemon_names.json", "w", encoding="utf-8") as file:

    json.dump(
        pokemon_names,
        file,
        indent=2,
        ensure_ascii=False
    )


print(f"Saved {len(pokemon_names)} Pokémon names.")