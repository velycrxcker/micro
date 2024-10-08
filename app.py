from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz
import pusher

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Página de inicio
@app.route("/")
def index():
    con.close()
    return render_template("app.html")

# Página para gestionar alumnos
@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

# Ruta para guardar los datos del alumno
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    if not con.is_connected():
        con.reconnect()
    
    matricula = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    cursor = con.cursor()

    sql = """
    INSERT INTO alumnos (Matricula, NombreApellido)
    VALUES (%s, %s)
    """
    val = (matricula, nombreapellido)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Ruta para buscar los registros de alumnos
@app.route("/alumnos/buscar", methods=["GET"])
def buscarAlumnos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT id, Matricula, NombreApellido, DATE_FORMAT(FechaRegistro, '%%d/%%m/%%Y') AS FechaRegistro
    FROM alumnos
    ORDER BY id DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()
    
    con.close()
    return make_response(jsonify(registros))

# Ruta para editar los datos de un alumno
@app.route("/alumnos/editar", methods=["GET"])
def editarAlumno():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT id, Matricula, NombreApellido
    FROM alumnos
    WHERE id = %s
    """
    val = (id,)
    
    cursor.execute(sql, val)
    registros = cursor.fetchall()
    
    con.close()
    return make_response(jsonify(registros))

# Ruta para eliminar un registro de alumno
@app.route("/alumnos/eliminar", methods=["POST"])
def eliminarAlumno():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor()
    sql = """
    DELETE FROM alumnos
    WHERE id = %s
    """
    val = (id,)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

if __name__ == "__main__":
    app.run(debug=True)
