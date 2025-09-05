from flask import Blueprint, render_template, request, redirect, jsonify

from src.utilidades.utils import datos_correctos, generarHash

from src.database.conexion import Conexion


bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	con=Conexion()

	# paises=con.obtenerPaises()
	paises=["España"]

	con.cerrarConexion()

	return render_template("registro.html",
							paises=paises)

@bp_registro.route("/ciudades_pais")
def obtenerCiudadesPais():

	pais=request.args.get("pais")

	if not pais:
		return jsonify({"error": "No se especificó el pais"}), 400

	con=Conexion()

	ciudades=con.obtenerCiudadesPais(pais, 25000)

	con.cerrarConexion()

	if ciudades:

		return jsonify(ciudades), 200

	else:
		
		return jsonify({"error": "Pais no encontrado"}), 404

@bp_registro.route("/singup", methods=["POST"])
def singup():

	usuario=request.form.get("usuario")
	correo=request.form.get("correo")
	contrasena=request.form.get("contrasena")
	nombre=request.form.get("nombre")
	apellido=request.form.get("apellido")
	fecha_nacimiento=request.form.get("fecha-nacimiento")
	pais=request.form.get("pais")
	ciudad=request.form.get("ciudad")

	if not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, correo):

		return redirect("/registro")

	con=Conexion()

	codigo_ciudad=con.obtenerCodigoCiudadPais(ciudad, pais)

	if con.existe_usuario(usuario) or not con.existe_codigo_ciudad(codigo_ciudad):

		con.cerrarConexion()

		return redirect("/registro")

	con.insertarUsuario(usuario, correo, generarHash(contrasena), nombre, apellido, fecha_nacimiento, codigo_ciudad)

	con.cerrarConexion()

	return render_template("singup.html", nombre=nombre)