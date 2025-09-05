import pytest

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "correo", "contrasena", "nombre", "apellido", "fecha_nacimiento", "codciudad"],
	[
		("nacho98", "nacho@correo", "1234", "nacho", "dorado", "1998-02-16", 103),
		("nacho948", "correo", "12vvnvvb34", "naegcho", "dordado", "1999-08-06", 1),
		("nacho", "micorreo@correo.es", "12vvn&fvvb34", "nachitoo", "dordado", "1998-02-16", 22)
	]
)
def test_insertar_usuario(conexion, usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, codciudad):

	conexion.insertarUsuario(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, codciudad)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion, numero_usuarios):

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion):

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	assert not conexion.existe_usuario("nacho99")

def test_existe_usuario_existen(conexion):

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	assert conexion.existe_usuario("nacho98")

def test_obtener_contrasena_usuario_no_existe(conexion):

	assert conexion.obtenerContrasenaUsuario("nacho98") is None

def test_obtener_contrasena_usuario_existen(conexion):

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	assert conexion.obtenerContrasenaUsuario("nacho98")=="1234"

def test_obtener_nombre_usuario_no_existe(conexion):

	assert conexion.obtenerNombre("nacho98") is None

def test_obtener_nombre_usuario_existen(conexion):

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	assert conexion.obtenerNombre("nacho98")=="nacho"

def test_obtener_admin_usuario_no_existe(conexion):

	assert not conexion.obtenerAdmin("nacho98")

def test_obtener_admin_usuario_no_admin(conexion):

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	assert not conexion.obtenerAdmin("nacho98")

def test_obtener_admin_usuario_si_admin(conexion):

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "1998-02-16", 103)

	conexion.c.execute("UPDATE usuarios SET Admin=True")

	conexion.confirmar()

	assert conexion.obtenerAdmin("nacho98")