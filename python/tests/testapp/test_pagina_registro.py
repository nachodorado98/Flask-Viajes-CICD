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
def test_pagina_singup_datos_incorrectos(cliente, conexion, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento, "ciudad":"Madrid",
											"pais":"España"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("naCho98",),("nacho",),("amanditaa",),("amanda99",)]
)
def test_pagina_singup_usuario_existente(cliente, conexion, usuario):

	conexion.insertarUsuario(usuario, "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", 103)

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid",
											"pais":"España"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["pais"],
	[("ESPAÑA",),("spain",),("Spain",),("Espana",)]
)
def test_pagina_singup_pais_no_existente(cliente, conexion, pais):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":"Madrid",
											"pais":pais})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["ciudad"],
	[("madrid",),("MADRID",),("Barna",),("Bcn",),("Tokio",),("tokyo",)]
)
def test_pagina_singup_ciudad_no_existente(cliente, conexion, ciudad):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"nacho@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"fecha-nacimiento":"1998-02-16", "ciudad":ciudad,
											"pais":"España"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "correo", "nombre", "apellido", "contrasena", "fecha_nacimiento", "ciudad", "pais"],
	[
		("nacho98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1999-07-16", "Madrid", "España"),
		("golnachoen98", "nacho@golden.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "Barcelona", "España"),
		("golden98", "nacho@gmail.es", "nachogol", "dorado", "Ab!Golden19&9", "1998-02-01", "Tokyo", "Japón"),
		("golde98", "nacho@gmail.es", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-05-16", "Sao Paulo", "Brasil"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "16&goldenNacho&98", "1998-02-16", "Los Angeles", "Estados Unidos"),
		("golden98", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2005-02-16", "Paris", "Francia"),
		("golden9", "nacho@gmail.es", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1990-02-16", "Madrid", "España")
	]
)
def test_pagina_singup_correcto(cliente, conexion, usuario, correo, nombre, apellido, contrasena, fecha_nacimiento, ciudad, pais):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"fecha-nacimiento":fecha_nacimiento, "ciudad":ciudad,
											"pais":pais})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert f"<p>Gracias por registrarte en nuestra plataforma, {nombre.title()}.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que proximamente podras acceder!</p>" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

def test_pagina_obtener_ciudades_pais_sin_pais(cliente):
	
	respuesta=cliente.get("/ciudades_pais")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==400
	assert "error" in contenido

def test_pagina_obtener_ciudades_pais_pais_no_existe(cliente):

	respuesta=cliente.get("/ciudades_pais?pais=no_existo")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==404
	assert "error" in contenido

def test_pagina_obtener_ciudades_pais(cliente):

	respuesta=cliente.get("/ciudades_pais?pais=España")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "error" not in contenido