#Importamos las librerias necesarias de Flask
from flask import Flask, render_template, request, url_for, redirect
#Importamos las clases de ConsultaUsuarios y ConsultaTareas
from consultas_bbdd import ConsultaUsuarios, ConsultaTareas

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
				#Insertamos el nuevo usuario con sus datos llamando a insertar_usuario_nuevo
				consulta_usuarios.insertar_usuario_nuevo(nombre, usuario, contrasena, correo)
				#Devolvemos el template de la pagina de bienvenida y pasamos el usuario y el correo
				return render_template("bienvenido.html", usuario=usuario, correo=correo)
			
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
	categorias=["Ocio", "Trabajo", "Pareja", "Familia", "Salud", "Deporte"]

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

#Condicion principal para la ejecucion del programa
if __name__=="__main__":
	#Corremos la app
	app.run(debug=True, port=4000)