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
EVOLUTION_CACHE = {}


def import_first_generation():
    validate_mongo_uri()

    for number in range(1, TOTAL_POKEMON + 1):
        pokemon_data = get_json(f"{POKEAPI_URL}/{number}")
        species_data = get_json(pokemon_data["species"]["url"])
        evolution_chain = get_evolution_chain(species_data)

        document = transform_pokemon(pokemon_data, species_data, evolution_chain)
        upsert_pokemon(document)

        print(f"Importado {number}: {document['name']}")
        time.sleep(0.1)

    print("Importacion finalizada")


def get_json(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def get_evolution_chain(species_data):
    url = species_data["evolution_chain"]["url"]

    if url not in EVOLUTION_CACHE:
        EVOLUTION_CACHE[url] = get_json(url)

    return EVOLUTION_CACHE[url]


def transform_pokemon(pokemon_data, species_data, evolution_chain):
    stats = {
        item["stat"]["name"]: item["base_stat"]
        for item in pokemon_data["stats"]
    }
    evolutions = get_evolution_info(pokemon_data["name"], evolution_chain)

    return {
        "pokedex_number": pokemon_data["id"],
        "name": pokemon_data["name"],
        "height": pokemon_data["height"] / 10,
        "weight": pokemon_data["weight"] / 10,
        "is_legendary": species_data.get("is_legendary", False),
        "is_mythical": species_data.get("is_mythical", False),
        "types": [item["type"]["name"] for item in pokemon_data["types"]],
        "abilities": [item["ability"]["name"] for item in pokemon_data["abilities"]],
        "description": get_spanish_description(species_data),
        "sprite": pokemon_data["sprites"]["front_default"] or "",
        "previous_evolutions": evolutions["previous_evolutions"],
        "next_evolutions": evolutions["next_evolutions"],
        "stats": {
            "hp": stats.get("hp", 0),
            "attack": stats.get("attack", 0),
            "defense": stats.get("defense", 0),
            "special_attack": stats.get("special-attack", 0),
            "special_defense": stats.get("special-defense", 0),
            "speed": stats.get("speed", 0),
        }
    }


def get_evolution_info(current_name, evolution_chain):
    evolution_map = {}

    def walk(node, previous):
        current = build_evolution_item(node["species"])
        next_evolutions = [
            build_evolution_item(child["species"])
            for child in node.get("evolves_to", [])
        ]

        evolution_map[current["name"]] = {
            "previous_evolutions": [previous] if previous else [],
            "next_evolutions": next_evolutions,
        }

        for child in node.get("evolves_to", []):
            walk(child, current)

    walk(evolution_chain["chain"], None)
    result = evolution_map.get(current_name)

    if not result:
        return {"previous_evolutions": [], "next_evolutions": []}

    return {
        "previous_evolutions": filter_first_generation(result["previous_evolutions"]),
        "next_evolutions": filter_first_generation(result["next_evolutions"]),
    }


def build_evolution_item(species):
    pokedex_number = extract_id_from_url(species["url"])

    return {
        "name": species["name"],
        "pokedex_number": pokedex_number,
        "sprite": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokedex_number}.png",
    }


def extract_id_from_url(url):
    return int(url.rstrip("/").split("/")[-1])


def filter_first_generation(evolutions):
    return [
        item
        for item in evolutions
        if item["pokedex_number"] <= TOTAL_POKEMON
    ]


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
