import pytest

def test_tabla_ciudades_llena(conexion):

	conexion.c.execute("SELECT * FROM ciudades")

	assert conexion.c.fetchall()

def test_obtener_ciudades_pais_no_existe(conexion):

	assert not conexion.obtenerCiudadesPais("No existo")

def test_obtener_ciudades_pais(conexion):

	assert conexion.obtenerCiudadesPais("España")

@pytest.mark.parametrize(["poblacion", "cantidad"],
	[(10000, 650),(100000, 61),(1000000, 2)]
)
def test_obtener_ciudades_pais_poblacion_limite(conexion, poblacion, cantidad):

	ciudades=conexion.obtenerCiudadesPais("España", poblacion)

	assert len(ciudades)==cantidad

@pytest.mark.parametrize(["ciudad", "pais"],
	[
		("Tokyo", "Pais"),
		("No Existo", "España"),
		("porto", "Portugal"),
		("BaRcElOnA",  "España"),
		("Madrid", "españa"),
		("Merida", "Mexico")
	]
)
def test_obtener_codigo_ciudad_pais_no_existe(conexion, ciudad, pais):

	assert not conexion.obtenerCodigoCiudadPais(ciudad, pais)

@pytest.mark.parametrize(["ciudad", "pais", "codigo_ciudad"],
	[
		("Tokyo", "Japón", 1),
		("Delhi", "India", 3),
		("Londres", "Reino Unido", 34),
		("Porto", "Portugal", 2438),
		("Barcelona", "España", 160),
		("Andorra la Vella", "Andorra", 809),
		("Madrid", "España", 103),
		("Merida Mex", "México", 917),
		("Merida", "España", 5809)
	]
)
def test_obtener_codigo_ciudad_pais(conexion, ciudad, pais, codigo_ciudad):

	assert conexion.obtenerCodigoCiudadPais(ciudad, pais)==codigo_ciudad