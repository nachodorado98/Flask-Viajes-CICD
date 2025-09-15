import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=DATABASE)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print(e)
			raise Exception("Error en la conexion a la BBDD")

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para vaciar la BBDD
	def vaciarBBDD(self)->None:

		self.c.execute("DELETE FROM usuarios")

		self.confirmar()

	# Metodo para obtener los paises
	def obtenerPaises(self)->List[str]:

		self.c.execute("""SELECT DISTINCT(pais)
	                 		FROM ciudades
	                 		ORDER BY pais""")

		paises=self.c.fetchall()

		return list(map(lambda pais: pais["pais"], paises))

	# Metodo para obtener las ciudades de un pais
	def obtenerCiudadesPais(self, pais:str, poblacion:int=0)->List[str]:

		self.c.execute("""SELECT ciudad
	                 		FROM ciudades 
	                 		WHERE pais=%s
	                 		AND poblacion>=%s
	                 		ORDER BY poblacion DESC""",
	                 		(pais, poblacion))

		ciudades=self.c.fetchall()

		return list(map(lambda ciudad: ciudad["ciudad"], ciudades))

	# Metodo para obtener el codigo de una ciudad de un pais concreto
	def obtenerCodigoCiudadPais(self, ciudad:str, pais:str)->Optional[int]:

		self.c.execute("""SELECT codciudad
							FROM ciudades
							WHERE ciudad=%s
							AND pais=%s""",
							(ciudad, pais))

		ciudad=self.c.fetchone()

		return None if ciudad is None else ciudad["codciudad"]

	# Metodo para comprobar si ya existe un usuario
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return False if not self.c.fetchone() else True

	# Metodo para comprobar si existe un codigo ciudad
	def existe_codigo_ciudad(self, codigo_ciudad:str)->bool:

		self.c.execute("""SELECT *
						FROM ciudades
						WHERE codciudad=%s""",
						(codigo_ciudad,))

		return False if not self.c.fetchone() else True

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, correo:str, contrasena:str, nombre:str,
						apellido:str, fecha_nacimiento:str, codciudad:int)->None:

		self.c.execute("""INSERT INTO usuarios
							VALUES (%s, %s, %s, %s, %s, %s, %s)""",
							(usuario, correo, contrasena, nombre, apellido, fecha_nacimiento, codciudad))

		self.confirmar()

	# Metodo para obtener la contrasena de un usuario
	def obtenerContrasenaUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return None if contrasena is None else contrasena["contrasena"]

	# Metodo para obtener el nombre de usuario
	def obtenerNombre(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT nombre
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		nombre=self.c.fetchone()

		return None if nombre is None else nombre["nombre"]

	# Metodo para obtener si el usuario es admin
	def obtenerAdmin(self, usuario:str)->bool:

		self.c.execute("""SELECT admin
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		admin=self.c.fetchone()

		return False if admin is None else admin["admin"]

	# Metodo para obtener los viajes de un usuario
	def obtenerViajes(self, usuario:str)->[List[Optional[tuple]]]:

		self.c.execute("""SELECT v.CodViaje, v.Usuario, c.Ciudad, c.CodCiudad, c.Pais, c.Siglas, v.Ida, v.Vuelta
							FROM Viajes v
							JOIN Ciudades c
							ON v.CodCiudad=c.CodCiudad
							WHERE Usuario=%s
							ORDER BY v.Ida DESC""",
							(usuario,))

		viajes=self.c.fetchall()

		# Funcion para convertir los datos de los viajes en el formato deseado
		def convertirDatos(datos:Dict)->tuple:

			ida=datos["ida"].strftime("%d/%m/%Y")

			vuelta=datos["vuelta"].strftime("%d/%m/%Y")

			return datos["codviaje"], datos["usuario"], datos["ciudad"], datos["codciudad"], datos["pais"], datos["siglas"], ida, vuelta

		return list(map(convertirDatos, viajes))

	# Metodo para insertar un viaje de un usuario
	def insertarViaje(self, codviaje:str, usuario:str, codciudad:int, ida:str, vuelta:str, hotel:str, web:str, transporte:str, comentario:str, imagen:str)->None:

		self.c.execute("""INSERT INTO Viajes VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
							(codviaje, usuario, codciudad, ida, vuelta, hotel, web, transporte, comentario, imagen))


		self.confirmar()