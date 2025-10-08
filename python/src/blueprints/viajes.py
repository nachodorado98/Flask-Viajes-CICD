from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.database.conexion import Conexion


bp_viajes=Blueprint("viajes", __name__)

@bp_viajes.route("/viajes")
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