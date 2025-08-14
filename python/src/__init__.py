from flask import Flask

from .blueprints.inicio import bp_inicio
from .blueprints.registro import bp_registro

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_registro)

	return app