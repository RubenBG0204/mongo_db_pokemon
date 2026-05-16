import os
import sys
import time

import requests


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from config.db import validate_mongo_uri  # noqa: E402
from models.pokemon_model import upsert_pokemon  # noqa: E402


POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"
TOTAL_POKEMON = 151


def import_first_generation():
    validate_mongo_uri()

    for number in range(1, TOTAL_POKEMON + 1):
        pokemon_data = get_json(f"{POKEAPI_URL}/{number}")
        species_data = get_json(pokemon_data["species"]["url"])

        document = transform_pokemon(pokemon_data, species_data)
        upsert_pokemon(document)

        print(f"Importado {number}: {document['name']}")
        time.sleep(0.1)

    print("Importacion finalizada")


def get_json(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def transform_pokemon(pokemon_data, species_data):
    stats = {
        item["stat"]["name"]: item["base_stat"]
        for item in pokemon_data["stats"]
    }

    return {
        "pokedex_number": pokemon_data["id"],
        "name": pokemon_data["name"],
        "height": pokemon_data["height"] / 10,
        "weight": pokemon_data["weight"] / 10,
        "is_legendary": species_data.get("is_legendary", False),
        "types": [item["type"]["name"] for item in pokemon_data["types"]],
        "abilities": [item["ability"]["name"] for item in pokemon_data["abilities"]],
        "description": get_spanish_description(species_data),
        "sprite": pokemon_data["sprites"]["front_default"] or "",
        "stats": {
            "hp": stats.get("hp", 0),
            "attack": stats.get("attack", 0),
            "defense": stats.get("defense", 0),
            "special_attack": stats.get("special-attack", 0),
            "special_defense": stats.get("special-defense", 0),
            "speed": stats.get("speed", 0),
        }
    }


def get_spanish_description(species_data):
    for entry in species_data.get("flavor_text_entries", []):
        if entry["language"]["name"] == "es":
            return clean_text(entry["flavor_text"])

    for entry in species_data.get("flavor_text_entries", []):
        if entry["language"]["name"] == "en":
            return clean_text(entry["flavor_text"])

    return "Sin descripcion"


def clean_text(text):
    return text.replace("\n", " ").replace("\f", " ").strip()


if __name__ == "__main__":
    try:
        import_first_generation()
    except RuntimeError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
