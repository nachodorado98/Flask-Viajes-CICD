import pytest
from flask_login import current_user

def test_pagina_inicio_sin_login(cliente):

	respuesta=cliente.get("/viajes", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho",),("nacho98",),("usuario_correcto",), ("amanda",)]
)
def test_pagina_inicio_con_login_usuario_no_existe(cliente, conexion, usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho", "contrasena": "Ab!CdEfGhIJK3LMN"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
	[("213214hhj&&ff",),("354354vff",),("2223321",), ("fdfgh&&55fjfkAfh",)]
)
def test_pagina_inicio_con_login_usuario_existe_contrasena_error(cliente, conexion, contrasena):

	cliente.post("/singup", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid",
											"pais":"España"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": contrasena})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_inicio_con_login_sin_viajes(cliente, conexion):

	cliente.post("/singup", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid",
											"pais":"España"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Aun no tienes ningun viaje que explorar, Nacho</h1>" in contenido
	assert not '<div class="card-container">' in contenido

def test_pagina_inicio_con_login_con_viaje(cliente, conexion):

	cliente.post("/singup", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid",
											"pais":"España"})

	conexion.insertarViaje("nacho98-1", "nacho98", 34, "2019-06-22", "2019-06-22", "Hotel", "Web", "Transporte", "comentario", "imagen.jpg")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Explora tus viajes, Nacho</h1>" in contenido
	assert '<div class="card-container">' in contenido

def test_pagina_logout(cliente, conexion):

	with cliente as cliente_abierto:

		cliente_abierto.post("/singup", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid",
											"pais":"España"})

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"})

		assert current_user.is_authenticated

		respuesta=cliente_abierto.get("/logout", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert not current_user.is_authenticated

		assert respuesta.status_code==200
		assert "<h1>Iniciar Sesión</h1>" in contenido