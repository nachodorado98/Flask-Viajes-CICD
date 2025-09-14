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
	assert '<div class="card">' in contenido
	assert '<div class="card-content">' in contenido
	assert '<h3 class="ciudad">' in contenido
	assert '<p class="pais">' in contenido
	assert '<p class="pais">' in contenido
	assert not "<h1>Aun no tienes ningun viaje que explorar, Nacho</h1>" in contenido