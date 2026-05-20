import os

from dotenv import load_dotenv
from flask import Flask

from routes.pokemon_routes import pokemon_bp


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "clave_desarrollo")

    app.register_blueprint(pokemon_bp)

    @app.errorhandler(RuntimeError)
    def handle_runtime_error(error):
        return f"<h1>Error de configuracion</h1><p>{error}</p>", 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
