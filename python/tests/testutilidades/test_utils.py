import pytest

from src.utilidades.utils import usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import fecha_correcta, correo_correcto, datos_correctos
from src.utilidades.utils import generarHash, comprobarHash

@pytest.mark.parametrize(["usuario"],
    [("ana-maria",),("carlos?456",),("",),(None,)]
)
def test_usuario_incorrecto(usuario):

    assert not usuario_correcto(usuario)

@pytest.mark.parametrize(["usuario"],
    [("juan123",),("usuario1",),("12345",),("ana_maria",),("carlos_456",)]
)
def test_usuario_correcto(usuario):

    assert usuario_correcto(usuario)

@pytest.mark.parametrize(["nombre"],
    [("123",),("Juan-Maria",),(None,),("",),("Nacho1998",)]
)
def test_nombre_incorrecto(nombre):

    assert not nombre_correcto(nombre)

@pytest.mark.parametrize(["nombre"],
    [("Nacho",),("Pérez",),("Ana",),("López",),("Carlos",),("González",),("Amanda",),("José",),("María del Carmen",)]
)
def test_nombre_correcto(nombre):

    assert nombre_correcto(nombre)

@pytest.mark.parametrize(["apellido"],
    [("123",),("Aranda.Gonzalez",),(None,),("",),("Dorado1998",)]
)
def test_apellido_incorrecto(apellido):

    assert not apellido_correcto(apellido)

@pytest.mark.parametrize(["apellido"],
    [("Nacho",),("Pérez",),("Ana",),("López",),("Carlos",),("González",),("Amanda",),("Aranda Gonzalez",)]
)
def test_apellido_correcto(apellido):

    assert apellido_correcto(apellido)

@pytest.mark.parametrize(["contrasena"],
    [("clave",),("CONTRASENA",),("12345678",),("Abcdefg",),("",),("A1b2C3d4",),("abcd",),("1234",),
     ("Ab CdEfGhI",),("Ab!CdEfGhI ",),(" Ab!CdEfGhI",),("Ab!CdEfGhIJKLMN",),("Ab@cdEfG",),
     ("Ab@cdEf1 G",),("Abcd12 34!",),(None,)]
)
def test_contrasena_incorrecta(contrasena):

    assert not contrasena_correcta(contrasena)

@pytest.mark.parametrize(["contrasena"],
    [("Ab!CdEfGhIJK3LMN",),("Abcd1234!",),("22&NachoD&19",)]
)
def test_contrasena_correcta(contrasena):

    assert contrasena_correcta(contrasena)

@pytest.mark.parametrize(["fecha"],
    [("1800-01-01",),("2100-01-01",),("1900-02-29",),("01-01-2000",),("2000/01/01",)]
)
def test_fecha_incorrecta(fecha):

    assert not fecha_correcta(fecha)

@pytest.mark.parametrize(["fecha"],
    [("1900-01-01",),("2005-01-01",),("2004-02-29",),("1998-02-16",),("1999-08-06",)]
)
def test_fecha_correcta(fecha):

    assert fecha_correcta(fecha)

@pytest.mark.parametrize(["correo"],
    [("correo_sin_arroba.com",),("usuario@sin_punto",),("correo@falta_punto_com",),("sin_local_part@.com",),("@falta_local_part.com",)]
)
def test_correo_incorrecto(correo):

    assert not correo_correcto(correo)

@pytest.mark.parametrize(["correo"],
    [("usuario@gmail.com",),("ejemplo123@yahoo.com",),("mi_correo-123@dominio.com",),
    ("usuario+etiqueta@dominio.com",), ("ejemplo.123@subdominio.dominio.co.uk",)]
)
def test_correo_correcto(correo):

    assert correo_correcto(correo)

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "fecha_nacimiento", "correo"],
    [
        (None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("golden98", None, "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho", None, "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho", "dorado", None, "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", None, "correo@correo.es"),
        ("carlos-456", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho", "dorado", "12345678", "1998-02-16", "correo@correo.es"),
        ("golden98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "2098-02-16", "correo@correo.es"),
        ("golden98", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@.es"),
    ]
)
def test_datos_incorrectos(usuario, nombre, apellido, contrasena, fecha_nacimiento, correo):

    assert not datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, correo)

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "fecha_nacimiento", "correo"],
    [
        ("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "usuario@gmail.com"),
        ("golden98", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "correo@correo.es"),
        ("carlos_456", "nachogolden", "dorado", "Ab!CdEfGhIJK3LMN", "1998-02-16", "ejemplo123@yahoo.com"),
    ]
)
def test_datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, correo):

    assert datos_correctos(usuario, nombre, apellido, contrasena, fecha_nacimiento, correo)

@pytest.mark.parametrize(["contrasena"],
    [("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_generar_hash_contrasena(contrasena):

    contrasena_hash=generarHash(contrasena)

    assert len(contrasena_hash)==60
    assert contrasena not in contrasena_hash

@pytest.mark.parametrize(["contrasena", "contrasena_mal"],
    [
        ("contrasena1234","contrasena123"),
        ("123456789","1234567899"),
        ("contrasena_secreta","contrasenasecreta")
    ]
)
def test_comprobar_hash_contrasena_incorrecta(contrasena, contrasena_mal):

    contrasena_hash=generarHash(contrasena)

    assert not comprobarHash(contrasena_mal, contrasena_hash)

@pytest.mark.parametrize(["contrasena"],
    [("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_comprobar_hash_contrasena_correcta(contrasena):

    contrasena_hash=generarHash(contrasena)

    assert comprobarHash(contrasena, contrasena_hash)