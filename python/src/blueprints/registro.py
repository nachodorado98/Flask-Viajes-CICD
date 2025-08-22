from flask import Blueprint, render_template, request, redirect

from src.utilidades.utils import datos_correctos

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	return render_template("registro.html")

@bp_registro.route("/singup", methods=["POST"])
def singup():

	usuario=request.form.get("usuario")
	correo=request.form.get("correo")
	contrasena=request.form.get("contrasena")
	nombre=request.form.get("nombre")
	apellido=request.form.get("apellido")
	fecha_nacimiento=request.form.get("fecha-nacimiento")

	if not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, correo):

		return redirect("/registro")

	return render_template("singup.html", nombre=nombre)