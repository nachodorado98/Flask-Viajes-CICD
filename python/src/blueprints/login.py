from flask import Blueprint, request, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user
from typing import Optional

from src.extensiones.manager import login_manager

from src.modelos.usuario import Usuario

from src.database.conexion import Conexion

from src.utilidades.utils import comprobarHash


bp_login=Blueprint("login", __name__)


# Funcion para comprobar y cargar  el usuario 
@login_manager.user_loader
def cargarUsuario(usuario:str)->Optional[Usuario]:

	con=Conexion()

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return None

	nombre=con.obtenerNombre(usuario)

	admin=con.obtenerAdmin(usuario)

	con.cerrarConexion()

	return Usuario(usuario, nombre, admin)

@bp_login.route("/login", methods=["GET", "POST"])
def login():

	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")

	con=Conexion()

	if not con.existe_usuario(usuario):

		con.cerrarConexion()

		return redirect("/")

	contrasena_hash_usuario=con.obtenerContrasenaUsuario(usuario)

	if not comprobarHash(contrasena, contrasena_hash_usuario):

		con.cerrarConexion()

		return redirect("/")

	nombre=con.obtenerNombre(usuario)

	admin=con.obtenerAdmin(usuario)

	con.cerrarConexion()

	usuario=Usuario(usuario, nombre, admin)

	login_user(usuario)

	siguiente=request.args.get("next")

	return redirect(siguiente or "/viajes")

@bp_login.route("/viajes")
@login_required
def pagina_viajes():

	usuario=current_user.id

	con=Conexion()

	viajes=con.obtenerViajes(usuario)

	con.cerrarConexion()

	return render_template("viajes.html",
							usuario=usuario,
							nombre=current_user.nombre,
							viajes=viajes)

@bp_login.route("/logout")
@login_required
def logout():

	logout_user()

	return redirect("/")