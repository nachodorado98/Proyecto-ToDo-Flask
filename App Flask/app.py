#Importamos las librerias necesarias de Flask
from flask import Flask, render_template, request, url_for, redirect
#Importamos las clases de ConsultaUsuarios y ConsultaTareas
from consultas_bbdd import ConsultaUsuarios, ConsultaTareas
#Importamos la clase Administrador
from admin import Administrador

#Creamos la app
app=Flask(__name__)

#Creamos las instancias de las dos clases importadas para realizar las consultas
consulta_usuarios=ConsultaUsuarios()
consulta_tareas=ConsultaTareas()

#Iniciamos el acceso en False
acceso=False

#Funcion para la pagina de inicio
@app.route("/")
def inicio():

	global acceso

	#Ponemos False al acceso por si viene de cerrar sesion
	acceso=False
	#Devolvemos el template de la pagina de inicio (para logearse)
	return render_template("base.html")

#Funcion para obtener las credenciales introducidas
@app.route("/login", methods=["GET","POST"])
def login():

	global acceso

	#Obtenemos las credenciales del usuario del formulario
	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")

	#Comprobamos que estan ambas introducidas
	if usuario and contrasena:
		#Comprobamos que las credenciales son correctas llamando a usuario_contrasena_correctos
		if consulta_usuarios.usuario_contrasena_correctos(usuario, contrasena):
			#Damos acceso
			acceso=True
			#Redireccionamos a la funcion del perfil pasando el usuario
			return redirect(url_for('perfil', usuario=usuario))
		#Si no son correctas redireccionamos a inicio
		else:
			return redirect(url_for("inicio"))
	#Si no estan introducidas redireccionamos a inicio
	else:
		return redirect(url_for("inicio"))

#Funcion para la pagina del registro
@app.route("/registro")
def registro():

	#Devolvemos el template del registro
	return render_template("registro.html")

#Funcion de la pagina de bienvenida
@app.route("/bienvenido", methods=["GET","POST"])
def bienvenido():

	global acceso

	#Probamos que no haya error en el registro
	try:
		#Obtenemos los datos del registro del formulario
		nombre=request.form.get("nombre").title()
		usuario=request.form.get("usuario")
		correo=request.form.get("correo")
		contrasena=request.form.get("contrasena")
		#Comprobamos que estan todos los datos introducidos
		if usuario and contrasena and correo and nombre:
			#Comprobamos que el usuario y correo son unicos llamando a usuario_correo_unicos
			if consulta_usuarios.usuario_correo_unicos(usuario, correo):
				#Damos acceso
				acceso=True
				#Comprobamos que se ha enviado o no el correo de confirmacion llamando a enviar_correo
				if Administrador.enviar_correo(nombre, usuario, correo):
					correo_confirmacion=f"Se ha enviado un correo de confirmacion a la direccion {correo}!!"
				else:
					correo_confirmacion=f"No se ha enviado un correo de confirmacion a la direccion {correo}!!"
	         
				#Insertamos el nuevo usuario con sus datos llamando a insertar_usuario_nuevo
				consulta_usuarios.insertar_usuario_nuevo(nombre, usuario, contrasena, correo)
				#Devolvemos el template de la pagina de bienvenida y pasamos el usuario y el correo
				return render_template("bienvenido.html", usuario=usuario, correo_confirmacion=correo_confirmacion)
			
			#Si el usuario o el correo no son unicos edireccionamos a la pagina del registro
			else:
				return redirect(url_for("registro"))

		#Si no estan introducidos todos reidreccionamos a la pagina del registro
		else:
			return redirect(url_for("registro"))
	
	#Si hay error redireccionamos a la pagina del registro
	except:
		return redirect(url_for("registro"))


#Funcion para la pagina del perfil del usuario
@app.route("/<usuario>")
def perfil(usuario):

	global acceso

	#Comprobamos que hay acceso
	if acceso:
		#Obtenemos las tareas no completadas del usuario del perfil llamando a tareas_no_completadas
		tareas=consulta_tareas.tareas_no_completadas(usuario)
		#Devolvemos el templete del perfil pasando el usuario y sus tareas no completadas
		return render_template("perfil.html", usuario=usuario, tareas=tareas)

	#Si no hay acceso redireccionamos a inicio
	else:
		return redirect(url_for("inicio"))

#Fucion para la pagina de insertar tarea nueva
@app.route("/<usuario>/insertartarea")
def insertar_tarea(usuario):

	global acceso

	#Categorias que se pueden seleccionar
	categorias=["Ocio", "Trabajo", "Pareja", "Familia", "Salud", "Deporte", "Estudios"]

	#Comprobamso que hay acceso
	if acceso:
		#Devolvemos el template de insertar la tarea pasandole el usuario y las categorias
		return render_template("insertar_tarea.html", usuario=usuario, categorias=categorias)
	
	#Si no hay acceso redireccionamos a inicio
	else:
		return redirect(url_for("inicio"))

#Funcion para obtener los datos de la tarea nueva a introducir
@app.route("/<usuario>/insertartarea/exito", methods=["GET","POST"])
def insertar_exito(usuario):

	#Probamos que no hay error en la nueva tarea
	try:
		#Obtenemos los datos de la tarea introducidos en el formulario
		titulo=request.form.get("titulo")
		descripcion=request.form.get("descripcion")
		categoria=request.form.get("categoria")

		#Comprobamos que estan todos los datos introducidos
		if titulo and descripcion and categoria:
			#Obtenemos el codigo del usuario que quiere introducir la tarea nueva llamando a codigo_usuario
			codigo=consulta_usuarios.codigo_usuario(usuario)
			#Insertamos la tarea con los datos obtenidos llamando a insertar_tarea
			consulta_tareas.insertar_tarea(titulo.title(), descripcion.title(), categoria, codigo)
			#Redireccionamos a la pagina del perfil pasandole el usuario
			return redirect(url_for("perfil", usuario=usuario))

		#Si no lo estan redireccionamos a la pagina de insertar la tarea
		else:
			return redirect(url_for("insertar_tarea"))

	#Si hay error redireccionamos a la pagina de inicio
	except:
		return redirect(url_for("inicio"))

#Funcion para completar una tarea mediante su codigo
@app.route("/<usuario>/completartarea<codtarea>")
def completar_tarea(usuario, codtarea):

	global acceso
	#Probamos que no hay error al completar
	try:
		#Comprobamso que hay acceso
		if acceso:
			#Obtenemos los datos de la tarea que se va a completar llamando a tarea_por_codigo
			tarea_a_completar=consulta_tareas.tarea_por_codigo(codtarea)
			#Obtenemos el codigo del usuario llamando a codigo_usuario
			codigo=consulta_usuarios.codigo_usuario(usuario)
			#Comprobamos que la tarea es del usuario llamando a comprobar_tarea_pertenece_usuario
			#Lo hacemos para que no se llegue a una tarea de otra persona por la url
			if consulta_tareas.comprobar_tarea_pertenece_usuario(codtarea, codigo):
				#Devolvemos el template de la pagina para completar la tarea pasando el usuario, la tarea y el codigo
				return render_template("completar_tarea.html", usuario=usuario, tarea_a_completar=tarea_a_completar, codtarea=codtarea)

			#Si no es la tarea del usuario redirecionamos a inicio
			else:
				return redirect(url_for("inicio"))
		#Si no hay acceso redireccionamos a inicio
		else:
			return redirect(url_for("inicio"))

	#Si hay error redireccionamos a la pagina de inicio
	except:
		return redirect(url_for("inicio"))


#Funcion para obtener los datos de la tarea nueva a introducir
@app.route("/<usuario>/completartareaexito<codtarea>", methods=["GET","POST"])
def insertar_tarea_completa(usuario, codtarea):

	#Probamos que no hay error en la nueva tarea
	try:
		#Obtenemos el comentario de la tarea introducidos en el formulario
		comentario=request.form.get("comentario")

		#Comprobamos que el comentario esta introducido
		if comentario:
			#Actualizamos la tarea poniendola completa y añadiendo el comentario llamando a completar_tarea_comentario
			consulta_tareas.completar_tarea_comentario(codtarea, comentario)
			return redirect(url_for("perfil", usuario=usuario))

		#Si no lo estan redireccionamos a la pagina de insertar la tarea
		else:
			return redirect(url_for("completar_tarea", usuario=usuario, codtarea=codtarea))

	#Si hay error redireccionamos a la pagina de inicio
	except:
		return redirect(url_for("inicio"))

#Funcion para la direccion de la pagina de las tareas completadas
@app.route("/<usuario>/tareascompletadas")
def tareas_completadas(usuario):
	global acceso

	#Probamos que no hay error al mostrar las tareas completas
	try:
		#Comprobamso que hay acceso
		if acceso:
			#Obtenemos las tareas completas del usuario llamando a tareas_completas_usuario
			tareas_completas=consulta_tareas.tareas_completas_usuario(usuario)
			#Devolvemos el template para ver la pagina de las tareas completadas pasandole el usuario y las tareas
			return render_template("completadas.html", usuario=usuario, tareas_completas=tareas_completas)

		#Si no hay acceso redireccionamos a inicio
		else:
			return redirect(url_for("inicio"))

	#Si hay error redireccionamos a la pagina de inicio
	except:
		return redirect(url_for("inicio"))


#Funcion para la pagina de detalle de la tarea
@app.route("/<usuario>/detalletarea<codtarea>")
def detalle_tarea(usuario, codtarea):

	global acceso
	#Probamos que no hay error al completar
	try:
		#Comprobamos que hay acceso
		if acceso:
			#Obtenemos los datos de la tarea que se va a detallar llamando a tarea_por_codigo
			tarea=consulta_tareas.tarea_por_codigo(codtarea)
			#Obtenemos el codigo del usuario llamando a codigo_usuario
			codigo=consulta_usuarios.codigo_usuario(usuario)
			#Comprobamos que la tarea es del usuario llamando a comprobar_tarea_pertenece_usuario
			#Lo hacemos para que no se llegue a una tarea de otra persona por la url
			if consulta_tareas.comprobar_tarea_pertenece_usuario(codtarea, codigo):
				#Devolvemos el template de la pagina para el detalle de la tarea pasando el usuario, la tarea y el codigo
				return render_template("detalle_tarea.html", usuario=usuario, tarea=tarea, codtarea=codtarea)
			
			#Si no es la tarea del usuario redirecionamos a inicio
			else:
				return redirect(url_for("inicio"))
		#Si no hay acceso redireccionamos a inicio
		else:
			return redirect(url_for("inicio"))

	#Si hay error redireccionamos a la pagina de inicio
	except:
		return redirect(url_for("inicio"))


#Funcion para borrar una tarea mediante su codigo
@app.route("/<usuario>/borrartarea<codtarea>")
def borrar_tarea(usuario, codtarea):

	global acceso
	#Probamos que no hay error al completar
	try:
		#Comprobamos que hay acceso
		if acceso:
			#Obtenemos los datos de la tarea que se va a borrar llamando a tarea_por_codigo
			tarea_a_borrar=consulta_tareas.tarea_por_codigo(codtarea)
			#Obtenemos el codigo del usuario llamando a codigo_usuario
			codigo=consulta_usuarios.codigo_usuario(usuario)
			#Comprobamos que la tarea es del usuario llamando a comprobar_tarea_pertenece_usuario
			#Lo hacemos para que no se llegue a una tarea de otra persona por la url
			if consulta_tareas.comprobar_tarea_pertenece_usuario(codtarea, codigo):
				#Devolvemos el template de la pagina para borrar la tarea pasando el usuario, la tarea y el codigo
				return render_template("borrar_tarea.html", usuario=usuario, tarea_a_borrar=tarea_a_borrar, codtarea=codtarea)

			#Si no es la tarea del usuario redirecionamos a inicio
			else:
				return redirect(url_for("inicio"))
		#Si no hay acceso redireccionamos a inicio
		else:
			return redirect(url_for("inicio"))

	#Si hay error redireccionamos a la pagina de inicio
	except:
		return redirect(url_for("inicio"))
	


#Funcion para borrar la tarea indicada
@app.route("/<usuario>/borrartareaexito<codtarea>", methods=["GET","POST"])
def borrar_exito(usuario, codtarea):

	#Probamos que no hay error en la eliminacion de la tarea
	#try:
		
	#Eliminamos la tarea llamando a eliminar_tarea
	consulta_tareas.eliminar_tarea(codtarea)
	#Redireccionamos a la pagina del perfil pasandole el usuario
	return redirect(url_for("perfil", usuario=usuario))

	#Si hay error redireccionamos a la pagina de inicio
	#except:
	#	return redirect(url_for("inicio"))	





#Condicion principal para la ejecucion del programa
if __name__=="__main__":
	#Corremos la app
	app.run(debug=True, port=4000)