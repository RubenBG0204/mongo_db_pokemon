from flask import Blueprint

from controllers.pokemon_controller import (
    create_pokemon_from_form,
    delete_pokemon_from_form,
    list_pokemon,
    show_create_form,
    show_edit_form,
    show_pokemon_detail,
    show_stats,
    update_pokemon_from_form,
)


pokemon_bp = Blueprint("pokemon", __name__)


@pokemon_bp.get("/")
def list_pokemon_route():
    return list_pokemon()


@pokemon_bp.get("/create")
def create_form_route():
    return show_create_form()


@pokemon_bp.post("/create")
def create_route():
    return create_pokemon_from_form()


@pokemon_bp.get("/edit/<pokemon_id>")
def edit_form_route(pokemon_id):
    return show_edit_form(pokemon_id)


@pokemon_bp.get("/pokemon/<pokemon_id>")
def detail_route(pokemon_id):
    return show_pokemon_detail(pokemon_id)


@pokemon_bp.post("/edit/<pokemon_id>")
def edit_route(pokemon_id):
    return update_pokemon_from_form(pokemon_id)


@pokemon_bp.post("/delete/<pokemon_id>")
def delete_route(pokemon_id):
    return delete_pokemon_from_form(pokemon_id)


@pokemon_bp.get("/stats")
def stats_route():
    return show_stats()
