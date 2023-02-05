#Clase para crear la Base de datos
class BaseDatos():

	def __init__(self, nombre_bbdd, bbdd, cursor):
		self.nombre_bbdd=nombre_bbdd
		self.bbdd=bbdd
		self.cursor=cursor

	#Crear la BBDD
	def crear_bbdd(self):
		self.cursor.execute(f"DROP DATABASE IF EXISTS {self.nombre_bbdd}")
		self.cursor.execute(f"CREATE DATABASE {self.nombre_bbdd}")

#Clase para crear cada Tabla	
class Tabla():
	
	def __init__(self, nombre, nombre_bbdd, bbdd, cursor):
		self.nombre=nombre
		self.nombre_bbdd=nombre_bbdd
		self.bbdd=bbdd
		self.cursor=cursor

	#Crear la tabla
	def crear_tabla(self, consulta):
		self.cursor.execute(f"USE {self.nombre_bbdd}")
		self.cursor.execute(f"DROP TABLE IF EXISTS {self.nombre}")
		self.cursor.execute(consulta)
		return True

