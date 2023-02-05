from config import Config

class ConsultaUsuarios():
	conexion=Config().crear_conexion()
	bbdd=conexion[0]
	c=conexion[1]

	def usuario_contrasena_correctos(self, usuario, contrasena):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""SELECT * 
						FROM Usuarios
						WHERE Usuario=%s
						AND Contraseña=%s""",
						(usuario, contrasena))

		if self.c.fetchone()!=None:
			return True
		else:
			return False


	def usuario_correo_unicos(self, usuario, correo):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""SELECT * 
						FROM Usuarios
						WHERE Usuario=%s
						OR Email=%s""",
						(usuario, correo))

		if self.c.fetchone()==None:
			return True
		else:
			return False

	def insertar_usuario_nuevo(self, nombre, usuario, contrasena, correo):
		self.c.execute("""USE tareasbbdd""")
		self.c.execute("""INSERT INTO Usuarios
						VALUES(%s, %s, %s, %s, %s)""",
						(None, nombre, usuario, contrasena, correo))

		self.bbdd.commit()