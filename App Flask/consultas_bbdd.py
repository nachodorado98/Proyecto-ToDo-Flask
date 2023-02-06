#Importamos la clase Config para la configiracion de MySQL
from config import Config

#Creamos la clase ConsultaUsuarios
class ConsultaUsuarios():

	#Creamos la conexion
	conexion=Config().crear_conexion()
	bbdd=conexion[0]
	c=conexion[1]

	#Funcion para comprobar que el usuario y contraseña son los correctos
	def usuario_contrasena_correctos(self, usuario, contrasena):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""SELECT * 
						FROM usuarios
						WHERE Usuario=%s
						AND Contraseña=%s""",
						(usuario, contrasena))

		#Si no devuelve None es que son correctos, devolvemos True
		if self.c.fetchone()!=None:
			return True
		#Si devuelve None es que no son correctos, devolvemos False
		else:
			return False

	#Funcion para comprobar que el usuario y el correo son unicos
	def usuario_correo_unicos(self, usuario, correo):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""SELECT * 
						FROM usuarios
						WHERE Usuario=%s
						OR Email=%s""",
						(usuario, correo))

		#Si devuelve None es que son unicos, devolvemos True
		if self.c.fetchone()==None:
			return True
		#Si no devuelve None es que no son unicos, devolvemos False
		else:
			return False

	#Funcion para insertar el usuario nuevo en la tabla usuarios
	def insertar_usuario_nuevo(self, nombre, usuario, contrasena, correo):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""INSERT INTO usuarios
						VALUES(%s, %s, %s, %s, %s)""",
						(None, nombre, usuario, contrasena, correo))

		self.bbdd.commit()

	#Funcion para obtener el codigo del usuario a partir de un usuario especifico
	def codigo_usuario(self, usuario):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""SELECT CodUsuario 
						FROM usuarios
						WHERE Usuario=%s""",
						(usuario,))
		return self.c.fetchone()[0]

class ConsultaTareas(ConsultaUsuarios):

	#Funcion para obtener las tareas no completadas de un usuario en concreto
	def tareas_no_completadas(self, usuario):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""SELECT t.CodTarea, t.Titulo, t.Descripcion, t.Categoria 
						FROM usuarios u
						JOIN tareas t
						ON u.CodUsuario=t.CodUsuario
						WHERE u.Usuario=%s
						AND t.Completada=0""",
						(usuario,))
		
		return self.c.fetchall()

	#Funcion para insertar una tarea de un usuario (no completa 0 y sin comentarios "")
	def insertar_tarea(self, titulo, descripcion, categoria, codigo):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""INSERT INTO tareas
						VALUES(%s, %s, %s, %s, %s, %s, %s)""",
						(None, titulo, descripcion, categoria, 0, "", codigo))

		self.bbdd.commit()