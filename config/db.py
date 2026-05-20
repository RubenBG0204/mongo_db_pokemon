import os
import sys

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, OperationFailure, ServerSelectionTimeoutError


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "pokemon_dam")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pokemon")
_cached_collection = None


def validate_mongo_uri():
    # Comprueba que la cadena de Atlas existe y no contiene placeholders.
    if not MONGO_URI:
        raise RuntimeError("Falta MONGO_URI en el archivo .env")

    placeholders = ["USUARIO", "PASSWORD", "CLUSTER", "PEGA_AQUI"]
    if any(text in MONGO_URI for text in placeholders):
        raise RuntimeError(
            "MONGO_URI todavia tiene datos de ejemplo. "
            "Pega tu cadena real de MongoDB Atlas en el archivo .env."
        )

    if not MONGO_URI.startswith(("mongodb+srv://", "mongodb://")):
        raise RuntimeError("MONGO_URI debe empezar por mongodb+srv:// o mongodb://")


def get_collection():
    global _cached_collection

    # Reutiliza la coleccion para no abrir conexiones repetidas.
    if _cached_collection is not None:
        return _cached_collection

    validate_mongo_uri()

    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=12000,
            tls=True,
            tlsCAFile=certifi.where()
        )
        # Fuerza una prueba real de conexion con Atlas.
        client.admin.command("ping")
    except ConfigurationError as error:
        raise RuntimeError(f"MONGO_URI no es valida: {error}") from error
    except OperationFailure as error:
        raise RuntimeError(
            "MongoDB Atlas rechazo la conexion. "
            "Revisa usuario, password y permisos del usuario de base de datos."
        ) from error
    except ServerSelectionTimeoutError as error:
        if "SSL handshake failed" in str(error):
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
            raise RuntimeError(
                "No se pudo completar la conexion TLS con MongoDB Atlas. "
                f"Estas usando Python {python_version}; para esta practica usa Python 3.12 o 3.13 "
                "y reinstala requirements.txt. Tambien revisa que tu IP este permitida en Atlas."
            ) from error

        raise RuntimeError(
            "No se pudo conectar con MongoDB Atlas. "
            "Revisa usuario, password, cluster y acceso de red en Atlas."
        ) from error

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Indices basicos para evitar duplicados y acelerar busquedas.
    collection.create_index("pokedex_number", unique=True)
    collection.create_index("name")

    _cached_collection = collection
    return _cached_collection


class LazyPokemonCollection:
    # Retrasa la conexion hasta que se usa la coleccion.
    def __getattr__(self, name):
        return getattr(get_collection(), name)


pokemon_collection = LazyPokemonCollection()
