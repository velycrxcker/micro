from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify, make_response
import mysql.connector

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para mostrar formulario de alumnos
@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Guardar un nuevo usuario o actualizar un usuario existente
@app.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form.get("id_usuario")  # Cambiado a id_usuario
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()

    try:
        if id_usuario:
            sql = """
            UPDATE usuarios SET
            Nombre_Usuario = %s,
            Contrasena = %s
            WHERE Id_Usuario = %s
            """
            val = (nombre_usuario, contrasena, id_usuario)
        else:
            sql = """
            INSERT INTO usuarios (Nombre_Usuario, Contrasena)
            VALUES (%s, %s)
            """
            val = (nombre_usuario, contrasena)

        cursor.execute(sql, val)
        con.commit()
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        con.close()

    return f"Usuario {nombre_usuario} guardado exitosamente."

# Buscar usuarios
@app.route("/usuarios/buscar")
def usuarios_buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM usuarios
    ORDER BY Id_Usuario DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()

    return make_response(jsonify(registros))

# Editar usuario
@app.route("/usuarios/editar", methods=["GET"])
def usuarios_editar():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.args.get("id_usuario")  # Cambiado a id_usuario

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM usuarios
    WHERE Id_Usuario = %s
    """
    val = (id_usuario,)

    cursor.execute(sql, val)
    registro = cursor.fetchone()
    con.close()

    return make_response(jsonify(registro))

# Eliminar usuario
@app.route("/usuarios/eliminar", methods=["POST"])
def usuarios_eliminar():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_usuario"]  # Cambiado a id_usuario

    cursor = con.cursor()
    sql = """
    DELETE FROM usuarios
    WHERE Id_Usuario = %s
    """
    val = (id_usuario,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return f"Usuario con ID {id_usuario} eliminado."

if __name__ == "__main__":
    app.run(debug=True)
