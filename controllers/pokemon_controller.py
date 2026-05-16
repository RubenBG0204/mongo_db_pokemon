from flask import redirect, render_template, request, url_for

from models.pokemon_model import (
    create_pokemon,
    delete_pokemon,
    get_all_pokemon,
    get_average_height,
    get_count_by_type,
    get_pokemon_by_id,
    update_pokemon,
)
from utils.filters import build_pokemon_filters


def list_pokemon():
    filters = build_pokemon_filters(request.args)
    pokemon = get_all_pokemon(filters)
    return render_template("index.html", pokemon=pokemon, filters=request.args)


def show_create_form():
    return render_template("create.html")


def create_pokemon_from_form():
    data = _form_to_document(request.form)
    create_pokemon(data)
    return redirect(url_for("pokemon.list_pokemon_route"))


def show_edit_form(pokemon_id):
    pokemon = get_pokemon_by_id(pokemon_id)
    return render_template("edit.html", pokemon=pokemon)


def show_pokemon_detail(pokemon_id):
    pokemon = get_pokemon_by_id(pokemon_id)
    return render_template("detail.html", pokemon=pokemon)


def update_pokemon_from_form(pokemon_id):
    data = _form_to_document(request.form)
    update_pokemon(pokemon_id, data)
    return redirect(url_for("pokemon.list_pokemon_route"))


def delete_pokemon_from_form(pokemon_id):
    delete_pokemon(pokemon_id)
    return redirect(url_for("pokemon.list_pokemon_route"))


def show_stats():
    average_height = get_average_height()
    count_by_type = get_count_by_type()
    return render_template(
        "stats.html",
        average_height=average_height,
        count_by_type=count_by_type
    )


def _form_to_document(form):
    types = [item.strip().lower() for item in form.get("types", "").split(",") if item.strip()]
    abilities = [item.strip().lower() for item in form.get("abilities", "").split(",") if item.strip()]

    return {
        "pokedex_number": int(form.get("pokedex_number", 0)),
        "name": form.get("name", "").strip().lower(),
        "height": float(form.get("height", 0)),
        "weight": float(form.get("weight", 0)),
        "is_legendary": form.get("is_legendary") == "on",
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
