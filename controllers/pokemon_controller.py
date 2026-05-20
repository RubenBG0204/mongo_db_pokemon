from flask import redirect, render_template, request, url_for

from models.pokemon_model import (
    create_pokemon,
    delete_pokemon,
    get_all_pokemon,
    get_average_height,
    get_count_by_type,
    get_pokemon_by_id,
    get_pokemon_by_number,
    get_top_total_stats,
    update_pokemon,
)
from utils.filters import build_pokemon_filters
from utils.mega_evolutions import add_mega_evolution_info, get_mega_evolution_fields


# Vista principal: aplica filtros y prepara la mejor stat para cada tarjeta.
def list_pokemon():
    filters = build_pokemon_filters(request.args)
    pokemon = get_all_pokemon(filters)
    pokemon = [_add_top_stat(item) for item in pokemon]
    return render_template("index.html", pokemon=pokemon, filters=request.args)


# Formularios y acciones CRUD.
def show_create_form():
    return render_template("create.html")


def create_pokemon_from_form():
    data = _form_to_document(request.form)
    create_pokemon(data)
    return redirect(url_for("pokemon.list_pokemon_route"))


def show_edit_form(pokemon_id):
    pokemon = get_pokemon_by_id(pokemon_id)
    # Completa informacion de megaevolucion antes de mostrar el formulario.
    pokemon = add_mega_evolution_info(pokemon)
    return render_template("edit.html", pokemon=pokemon)


def show_pokemon_detail(pokemon_id):
    pokemon = get_pokemon_by_id(pokemon_id)
    # Completa informacion calculada que no siempre esta guardada.
    pokemon = add_mega_evolution_info(pokemon)
    return render_template("detail.html", pokemon=pokemon)


def show_pokemon_detail_by_number(pokedex_number):
    pokemon = get_pokemon_by_number(pokedex_number)
    pokemon = add_mega_evolution_info(pokemon)
    return render_template("detail.html", pokemon=pokemon)


def update_pokemon_from_form(pokemon_id):
    data = _form_to_document(request.form)
    update_pokemon(pokemon_id, data)
    return redirect(url_for("pokemon.list_pokemon_route"))


def delete_pokemon_from_form(pokemon_id):
    delete_pokemon(pokemon_id)
    return redirect(url_for("pokemon.list_pokemon_route"))


def show_stats():
    # Datos preparados con aggregation framework.
    average_height = get_average_height()
    count_by_type = get_count_by_type()
    top_total_stats = get_top_total_stats()
    return render_template(
        "stats.html",
        average_height=average_height,
        count_by_type=count_by_type,
        top_total_stats=top_total_stats
    )


def _form_to_document(form):
    # Convierte datos del formulario HTML en documento MongoDB.
    types = [item.strip().lower() for item in form.get("types", "").split(",") if item.strip()]
    abilities = [item.strip().lower() for item in form.get("abilities", "").split(",") if item.strip()]
    name = form.get("name", "").strip().lower()
    mega_fields = get_mega_evolution_fields(
        name,
        force=form.get("can_mega_evolve") == "on",
        detect_known=True,
    )

    return {
        "pokedex_number": int(form.get("pokedex_number", 0)),
        "name": name,
        "height": float(form.get("height", 0)),
        "weight": float(form.get("weight", 0)),
        "is_legendary": form.get("is_legendary") == "on",
        "is_mythical": form.get("is_mythical") == "on",
        "can_mega_evolve": mega_fields["can_mega_evolve"],
        "mega_stones": mega_fields["mega_stones"],
        "types": types,
        "abilities": abilities,
        "description": form.get("description", "").strip(),
        "sprite": form.get("sprite", "").strip(),
        "stats": {
            "hp": int(form.get("hp", 0)),
            "attack": int(form.get("attack", 0)),
            "defense": int(form.get("defense", 0)),
            "special_attack": int(form.get("special_attack", 0)),
            "special_defense": int(form.get("special_defense", 0)),
            "speed": int(form.get("speed", 0)),
        }
    }


def _add_top_stat(pokemon):
    # Calcula la stat mas alta que se muestra en la tarjeta.
    stats = pokemon.get("stats", {})
    candidates = {
        "Vida": stats.get("hp", 0),
        "Ataque": stats.get("attack", 0),
        "Defensa": stats.get("defense", 0),
        "Ataque especial": stats.get("special_attack", 0),
        "Defensa especial": stats.get("special_defense", 0),
    }
    top_name, top_value = max(candidates.items(), key=lambda item: item[1])
    pokemon["top_stat_name"] = top_name
    pokemon["top_stat_value"] = top_value
    return pokemon
