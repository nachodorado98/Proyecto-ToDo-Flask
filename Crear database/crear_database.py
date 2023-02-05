from config import Config
from consultas_crear_bbdd import BaseDatos, Tabla

#Creamos la conexion con MySQL
conexion=Config().crear_conexion()
bbdd=conexion[0]
c=conexion[1]

#--------------------------------------------BASE DE DATOS---------------------------------------
nombre_bbdd="tareasbbdd"
#creacion_bbdd=BaseDatos(nombre_bbdd, bbdd, c)
#creacion_bbdd.crear_bbdd()


#--------------------------------------------TABLA USUARIOS-----------------------------------------
tabla_usuarios=Tabla("usuarios", nombre_bbdd, bbdd, c)
consulta_tabla_usuarios="""CREATE TABLE usuarios
						(CodUsuario INT AUTO_INCREMENT,
						Nombre VARCHAR(20),
						Usuario VARCHAR(20),
						Contraseña VARCHAR(32),
						Email VARCHAR(20),
						PRIMARY KEY (Codusuario))"""
#creacion_tabla_usuarios=tabla_usuarios.crear_tabla(consulta_tabla_usuarios)


#--------------------------------------------TABLA TAREAS-----------------------------------------
tabla_tareas=Tabla("tareas", nombre_bbdd, bbdd, c)
consulta_tabla_tareas="""CREATE TABLE tareas
						(CodTarea INT AUTO_INCREMENT,
						Titulo VARCHAR(50),
						Descripcion VARCHAR(200),
						Categoria VARCHAR(50),
						Completada BIT DEFAULT 0,
						Comentarios VARCHAR(200),
						CodUsuario INT,
						PRIMARY KEY (CodTarea),
						FOREIGN KEY (CodUsuario) REFERENCES usuarios (CodUsuario) ON DELETE CASCADE)"""
#creacion_tabla_tareas=tabla_tareas.crear_tabla(consulta_tabla_tareas)