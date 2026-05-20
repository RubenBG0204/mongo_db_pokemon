import requests


POKEAPI_POKEMON_URL = "https://pokeapi.co/api/v2/pokemon"
EVOLUTION_CACHE = {}


def get_empty_evolutions():
    # Estructura por defecto si no hay evoluciones o falla la API.
    return {"previous_evolutions": [], "next_evolutions": []}


def fetch_evolutions_from_pokeapi(name, pokedex_number=0):
    # Busca en PokeAPI la cadena evolutiva del Pokemon indicado.
    lookups = [name.strip().lower(), str(pokedex_number)]

    lookups = [item for item in lookups if item and item != "0"]

    if not lookups:
        return get_empty_evolutions()

    for lookup in lookups:
        try:
            pokemon_data = get_json(f"{POKEAPI_POKEMON_URL}/{lookup}")
            species_data = get_json(pokemon_data["species"]["url"])
            evolution_chain = get_evolution_chain(species_data)
            return get_evolution_info(pokemon_data["name"], evolution_chain)
        except (KeyError, requests.RequestException, ValueError):
            continue

    return get_empty_evolutions()


def add_evolution_info(pokemon):
    # Rellena evoluciones si el documento todavia no las tiene.
    if not pokemon:
        return pokemon

    previous = pokemon.get("previous_evolutions", [])
    next_items = pokemon.get("next_evolutions", [])

    if previous or next_items:
        return pokemon

    evolutions = fetch_evolutions_from_pokeapi(
        pokemon.get("name", ""),
        pokemon.get("pokedex_number", 0),
    )
    pokemon["previous_evolutions"] = evolutions["previous_evolutions"]
    pokemon["next_evolutions"] = evolutions["next_evolutions"]
    return pokemon


def get_json(url):
    # Peticion HTTP sencilla con timeout y control de errores.
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def get_evolution_chain(species_data):
    # Cachea cadenas evolutivas para no repetir llamadas a PokeAPI.
    url = species_data["evolution_chain"]["url"]

    if url not in EVOLUTION_CACHE:
        EVOLUTION_CACHE[url] = get_json(url)

    return EVOLUTION_CACHE[url]


def get_evolution_info(current_name, evolution_chain):
    # Recorre todo el arbol evolutivo, sin limitarlo a una generacion.
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
    return evolution_map.get(current_name, get_empty_evolutions())


def build_evolution_item(species):
    # Datos minimos para pintar miniatura y enlace.
    pokedex_number = extract_id_from_url(species["url"])

    return {
        "name": species["name"],
        "pokedex_number": pokedex_number,
        "sprite": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokedex_number}.png",
    }


def extract_id_from_url(url):
    # Extrae el numero final de una URL de PokeAPI.
    return int(url.rstrip("/").split("/")[-1])
