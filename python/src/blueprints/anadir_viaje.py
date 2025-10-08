from flask import Blueprint, render_template
from flask_login import login_required, current_user

from datetime import datetime

from src.database.conexion import Conexion


bp_anadir_viaje=Blueprint("anadir_viaje", __name__)

@bp_anadir_viaje.route("/anadir_viaje")
@login_required
def pagina_anadir_viaje():

	usuario=current_user.id

	con=Conexion()

	paises=con.obtenerPaises()

	con.cerrarConexion()

	return render_template("anadir_viaje.html",
							usuario=usuario,
							nombre=current_user.nombre,
							paises=paises,
							fecha_hoy=datetime.now().strftime("%Y-%m-%d"))