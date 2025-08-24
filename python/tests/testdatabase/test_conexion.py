import pytest

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_viajes_cicd"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "usuarios" in tablas 
	assert "paises" in tablas
	assert "ciudades" in tablas
	
def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_vaciar_bbdd(conexion):

	tablas=["usuarios"]

	conexion.insertarUsuario("golden98", "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", 103)

	for tabla in tablas:

		conexion.c.execute(f"SELECT * FROM {tabla}")

		assert conexion.c.fetchall()

	conexion.vaciarBBDD()

	for tabla in tablas:

		conexion.c.execute(f"SELECT * FROM {tabla}")

		assert not conexion.c.fetchall()