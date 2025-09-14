import pytest

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_viajes_cicd"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "usuarios" in tablas 
	assert "paises" in tablas
	assert "ciudades" in tablas
	assert "viajes" in tablas
	
def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_vaciar_bbdd(conexion_usuario_viaje):

	tablas=["usuarios", "viajes"]

	for tabla in tablas:

		conexion_usuario_viaje.c.execute(f"SELECT * FROM {tabla}")

		assert conexion_usuario_viaje.c.fetchall()

	conexion_usuario_viaje.vaciarBBDD()

	for tabla in tablas:

		conexion_usuario_viaje.c.execute(f"SELECT * FROM {tabla}")

		assert not conexion_usuario_viaje.c.fetchall()