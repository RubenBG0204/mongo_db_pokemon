from datetime import datetime

from bson import ObjectId

from config.db import pokemon_collection


def get_all_pokemon(filters=None):
    filters = filters or {}
    return list(pokemon_collection.find(filters).sort("pokedex_number", 1))


def get_pokemon_by_id(pokemon_id):
    return pokemon_collection.find_one({"_id": ObjectId(pokemon_id)})


def create_pokemon(data):
    now = datetime.utcnow()
    data["created_at"] = now
    data["updated_at"] = now
    return pokemon_collection.insert_one(data)


def update_pokemon(pokemon_id, data):
    data["updated_at"] = datetime.utcnow()
    return pokemon_collection.update_one(
        {"_id": ObjectId(pokemon_id)},
        {"$set": data}
    )


def delete_pokemon(pokemon_id):
    return pokemon_collection.delete_one({"_id": ObjectId(pokemon_id)})


def upsert_pokemon(data):
    now = datetime.utcnow()
    data["updated_at"] = now

    pokemon_collection.update_one(
        {"pokedex_number": data["pokedex_number"]},
        {
            "$set": data,
            "$setOnInsert": {"created_at": now}
        },
        upsert=True
    )


def get_average_height():
    pipeline = [
        {"$match": {"height": {"$exists": True}}},
        {
            "$group": {
                "_id": None,
                "average_height": {"$avg": "$height"},
                "total": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "average_height": {"$round": ["$average_height", 2]},
                "total": 1
            }
        }
    ]
    result = list(pokemon_collection.aggregate(pipeline))
    return result[0] if result else {"average_height": 0, "total": 0}


def get_count_by_type():
    pipeline = [
        {"$match": {"types": {"$exists": True}}},
        {"$unwind": "$types"},
        {
            "$group": {
                "_id": "$types",
                "total": {"$sum": 1}
            }
        },
        {"$sort": {"total": -1, "_id": 1}},
        {
            "$project": {
                "_id": 0,
                "type": "$_id",
                "total": 1
            }
        }
    ]
    return list(pokemon_collection.aggregate(pipeline))
