from flask import Flask, render_template, request, jsonify, make_response
import pusher
import mysql.connector

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

@app.route("/usuarios/buscar")
def buscar_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()

    con.close()
    return make_response(jsonify(registros))

@app.route("/usuarios/guardar", methods=["POST"])
def guardar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_usuario"]
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()

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
    con.close()

    notificar_actualizacion_usuarios()

    return make_response(jsonify({}))

@app.route("/usuarios/editar", methods=["GET"])
def editar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.args["id_usuario"]

    cursor = con.cursor(dictionary=True)
    sql = "SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_usuario"]

    cursor = con.cursor()
    sql = "DELETE FROM usuarios WHERE Id_Usuario = %s"
    val = (id_usuario,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificar_actualizacion_usuarios()

    return make_response(jsonify({}))

# Función para notificar actualizaciones a través de Pusher
def notificar_actualizacion_usuarios():
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="2df86616075904231311",
        secret="2f91d936fd43d8e85a1a",
        cluster="us2",
        ssl=True
    )
    pusher_client.trigger("canalUsuarios", "registroUsuarios", {})

if __name__ == "__main__":
    app.run(debug=True)
