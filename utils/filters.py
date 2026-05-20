def build_pokemon_filters(args):
    # Construye el diccionario de filtros que entiende MongoDB.
    filters = {}

    name = args.get("name", "").strip()
    description = args.get("description", "").strip()
    min_height = args.get("min_height", "").strip()
    max_height = args.get("max_height", "").strip()
    types = args.get("types", "").strip()
    types_size = args.get("types_size", "").strip()
    has_sprite = args.get("has_sprite", "").strip()

    if name:
        # $regex permite buscar texto parcial sin distinguir mayusculas.
        filters["name"] = {"$regex": name, "$options": "i"}

    if description:
        filters["description"] = {"$regex": description, "$options": "i"}

    # $gt y $lt filtran alturas mayores o menores.
    height_filter = {}
    if min_height:
        height_filter["$gt"] = float(min_height)
    if max_height:
        height_filter["$lt"] = float(max_height)
    if height_filter:
        filters["height"] = height_filter

    if types:
        selected_types = [item.strip().lower() for item in types.split(",") if item.strip()]
        if selected_types:
            # $in busca Pokemon que tengan cualquiera de los tipos indicados.
            filters["types"] = {"$in": selected_types}

    if types_size:
        # $size filtra por cantidad exacta de tipos.
        filters["types"] = {"$size": int(types_size)}

    if has_sprite == "yes":
        # $exists comprueba si el campo existe en MongoDB.
        filters["sprite"] = {"$exists": True, "$ne": ""}
    elif has_sprite == "no":
        filters["sprite"] = {"$exists": False}

    return filters
