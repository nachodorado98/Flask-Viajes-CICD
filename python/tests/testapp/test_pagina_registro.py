import pytest

def test_pagina_registro(cliente):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento"],
	[
		(None, "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", None, "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", None, "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", None, "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", None),
		("carlos-456", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "12345678", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2098-02-16")
	]
)
def test_pagina_singup_datos_incorrectos(cliente, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento"],
	[
		("nacho98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1999-07-16"),
		("golnachoen98", "nacho@golden.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nachogol", "dorado", "Ab!Golden19&9", "1998-02-01"),
		("golde98", "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-05-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "16&goldenNacho&98", "1998-02-16"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2005-02-16"),
		("golden9", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1990-02-16")
	]
)
def test_pagina_singup_correcto(cliente, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert f"<p>Gracias por registrarte en nuestra plataforma, {nombre.title()}.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que proximamente podras acceder!</p>" in contenido