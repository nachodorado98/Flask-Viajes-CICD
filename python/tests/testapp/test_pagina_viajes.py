import pytest

def test_pagina_viajes_sin_viajes(cliente, conexion_usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert not "<h1>Explora tus viajes, Nacho</h1>" in contenido
	assert not '<div class="card-container">' in contenido
	assert not '<div class="card">' in contenido
	assert not '<div class="card-content">' in contenido
	assert not '<h3 class="ciudad">' in contenido
	assert not '<p class="pais">' in contenido
	assert not '<p class="pais">' in contenido
	assert "<h1>Aun no tienes ningun viaje que explorar, Nacho</h1>" in contenido

def test_pagina_viajes_con_viaje(cliente, conexion_usuario_viaje):

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Explora tus viajes, Nacho</h1>" in contenido
	assert '<div class="card-container">' in contenido
	assert '<div class="card"' in contenido
	assert 'style="--bandera:' in contenido
	assert "/static/imagenes/banderas/GBR.png" in contenido
	assert '<div class="card-content">' in contenido
	assert '<h3 class="ciudad">' in contenido
	assert '<p class="pais">' in contenido
	assert '<p class="pais">' in contenido
	assert not "<h1>Aun no tienes ningun viaje que explorar, Nacho</h1>" in contenido

@pytest.mark.parametrize(["ciudad", "bandera"],
	[
		(34, "GBR"),
		(1, "JPN"),
		(5, "BRA"),
		(35, "FRA"),
		(103, "ESP"),
		(22, "PAK")
	]
)
def test_pagina_viajes_bandera_viaje(cliente, conexion_usuario, ciudad, bandera):

	conexion_usuario.insertarViaje(f"nacho98-{ciudad}", "nacho98", ciudad, '2019-06-22', '2019-06-22', 'Hotel', 'Web', 'Transporte', 'Comentario', 'imagen.jpg')

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Explora tus viajes, Nacho</h1>" in contenido
	assert '<div class="card-container">' in contenido
	assert '<div class="card"' in contenido
	assert 'style="--bandera:' in contenido
	assert f"/static/imagenes/banderas/{bandera}.png" in contenido
	assert '<div class="card-content">' in contenido
	assert '<h3 class="ciudad">' in contenido
	assert '<p class="pais">' in contenido
	assert '<p class="pais">' in contenido
	assert not "<h1>Aun no tienes ningun viaje que explorar, Nacho</h1>" in contenido