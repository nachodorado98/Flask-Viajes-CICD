import pytest

def test_pagina_anadir_viaje_sin_login(cliente):

	respuesta=cliente.get("/anadir_viaje", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_anadir_viaje(cliente):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/anadir_viaje")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "<h1>Añadir Nuevo Viaje</h1>" in contenido
		assert '<div class="container viaje-form-container">' in contenido
		assert '<div id="resumen-modal" class="modal">' in contenido
		assert '<h2>Resumen del Viaje</h2>' in contenido
		assert '<div id="resumen-detalle" class="resumen-grid"></div>' in contenido