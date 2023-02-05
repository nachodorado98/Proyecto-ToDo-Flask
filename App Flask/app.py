from flask import Flask, render_template, request, url_for, redirect
from consultas_bbdd import ConsultaUsuarios

app=Flask(__name__)

consulta_usuarios=ConsultaUsuarios()

@app.route("/")
def inicio():
	return render_template("base.html")

@app.route("/login", methods=["GET","POST"])
def login():

	usuario=request.form.get("usuario")
	contrasena=request.form.get("contrasena")
	if usuario and contrasena:
		if consulta_usuarios.usuario_contrasena_correctos(usuario, contrasena):
			return redirect(url_for('perfil', user=usuario))
		else:
			return redirect(url_for("inicio"))
	else:
		return redirect(url_for("inicio"))

@app.route("/registro")
def registro():

	return render_template("registro.html")

@app.route("/bienvenido", methods=["GET","POST"])
def bienvenido():

	nombre=request.form.get("nombre").title()
	usuario=request.form.get("usuario")
	correo=request.form.get("correo")
	contrasena=request.form.get("contrasena")
	if usuario and contrasena and correo and nombre:
		if consulta_usuarios.usuario_correo_unicos(usuario, correo):
			consulta_usuarios.insertar_usuario_nuevo(nombre, usuario, contrasena, correo)
			return render_template("bienvenido.html", usuario=usuario, correo=correo)
		else:
			return redirect(url_for("registro"))

	else:
		return redirect(url_for("registro"))


@app.route("/perfil/<user>")
def perfil(user):

	return f"<p>{user}</p>"



if __name__=="__main__":
	app.run(debug=True, port=4000)