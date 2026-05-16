# Pokémon DAM MongoDB

Aplicación web con Flask, PyMongo y MongoDB Atlas que importa los 151 primeros Pokémon desde PokéAPI.

## Funcionalidades

- Importación de Pokémon desde PokéAPI.
- CRUD completo.
- Filtros avanzados con MongoDB.
- Estadísticas con aggregation framework.
- Vista de detalle con estadísticas completas.

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Copia `.env.example` como `.env` y completa `MONGO_URI` con tu conexión de MongoDB Atlas.

## Importar datos

```powershell
python scripts\import_pokemon.py
```

## Ejecutar la app

```powershell
python app.py
```

Abre:

```text
http://127.0.0.1:5000
```

También puedes usar:

```powershell
.\import_pokemon.bat
.\run_app.bat
```
