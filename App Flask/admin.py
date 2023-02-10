#Importamos la libreria que nos permite enviar correos
import smtplib
#Importamos el os
import os


#Clase para realizar las tareas del administrador
class Administrador():
	
	#Funcion para enviar el correo de confirmacion
	@staticmethod
	def enviar_correo(nombre, usuario, correo):
		#Obtenemos el valor de las variables de entorno del correo y la contraseña
		correo_tarea=os.environ.get("CORREO_ATM")
		contrasena_tarea=os.environ.get("CONTRASENA_ATM")
		mensaje=f"""From:{correo_tarea}
		To:{correo}
		Subject:SUBSCRIPCION A ToDo WEB\n
		Bienvenido {nombre}!
		Te has subscrito a la pagina web con el nombre de usuario: {usuario}
		"""
		#Intentamos enviar el correo
		try:
			server=smtplib.SMTP("smtp.gmail.com",587)
			server.starttls()
			server.login(correo_tarea, contrasena_tarea)
			server.sendmail(correo_tarea, correo, mensaje)
			return True
		except:
			return False



    

