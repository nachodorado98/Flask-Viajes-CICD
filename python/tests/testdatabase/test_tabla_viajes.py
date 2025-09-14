import pytest

def test_tabla_viajes_vacia(conexion):

	conexion.c.execute("SELECT * FROM viajes")

	assert conexion.c.fetchall()==[]

@pytest.mark.parametrize(["codigo_ciudad", "ida", "vuelta", "hotel", "web", "transporte", "comentario", "imagen"],
	[
		(1, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "Comentario", "hjhjhjjhhj.jpg"),
		(34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen"),
		(160, "2023-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "Sin Comentario", "Sin Imagen"),
		(2438, "2023-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "asdfghjkl", "madrid_españa_jjjjkjbj.png")
	]
)
def test_insertar_viaje(conexion_usuario, codigo_ciudad, ida, vuelta, hotel, web, transporte, comentario, imagen):

	conexion_usuario.insertarViaje(f"nacho98-{codigo_ciudad}", "nacho98", codigo_ciudad, ida, vuelta, hotel, web, transporte, comentario, imagen)

	conexion_usuario.c.execute("SELECT * FROM viajes")

	viajes=conexion_usuario.c.fetchall()

	viaje=viajes[0]

	assert len(viajes)==1
	assert viaje["codciudad"]==codigo_ciudad
	assert viaje["ida"].strftime("%Y-%m-%d")==ida
	assert viaje["vuelta"].strftime("%Y-%m-%d")==vuelta
	assert viaje["hotel"]==hotel
	assert viaje["web"]==web
	assert viaje["transporte"]==transporte
	assert viaje["comentario"]==comentario
	assert viaje["imagen"]==imagen

def test_insertar_viajes(conexion_usuario):

	for numero in range(5):

		conexion_usuario.insertarViaje(f"nacho98-{numero}", "nacho98", 34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg"),

	conexion_usuario.c.execute("SELECT * FROM viajes")

	viajes=conexion_usuario.c.fetchall()

	assert len(viajes)==5

def test_obtener_viajes_no_existe_usuario(conexion):

	assert not conexion.obtenerViajes("nacho98")

def test_obtener_viajes_no_existentes(conexion_usuario):

	assert not conexion_usuario.obtenerViajes("nacho98")

def test_obtener_viajes_otro_usuario(conexion_usuario):

	conexion_usuario.insertarViaje("nacho98-34", "nacho98", 34, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte', 'Comentario', 'Imagen')

	assert not conexion_usuario.obtenerViajes("nacho")

@pytest.mark.parametrize(["codigo_ciudad"],
	[(1,),(22,),(2019,),(13,)]
)
def test_obtener_viajes_existente(conexion_usuario, codigo_ciudad):

	conexion_usuario.insertarViaje(f"nacho98-{codigo_ciudad}", "nacho98", codigo_ciudad, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte', 'Comentario', 'Imagen')

	viajes=conexion_usuario.obtenerViajes("nacho98")

	assert len(viajes)==1
	assert viajes[0][3]==codigo_ciudad

def test_obtener_viajes_existentes(conexion_usuario):

	for codigo_ciudad in range(1, 11):

		conexion_usuario.insertarViaje(f"nacho98-{codigo_ciudad}", "nacho98", codigo_ciudad, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte', 'Comentario', 'Imagen')

	viajes=conexion_usuario.obtenerViajes("nacho98")

	assert len(viajes)==10

	for numero, viaje in enumerate(viajes):

		assert viaje[3]==(numero+1)

	assert viajes[0][0]<viajes[-1][0]