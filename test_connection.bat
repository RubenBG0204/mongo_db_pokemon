@echo off
call .venv\Scripts\activate
python -c "from config.db import get_collection; c=get_collection(); print('Conexion correcta:', c.full_name)"
