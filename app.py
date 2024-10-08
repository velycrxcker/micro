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
        return jsonify({"success": True, "message": "Usuario guardado exitosamente."})  # Cambiado aquí
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500  # Manejo de errores
    finally:
        cursor.close()
        con.close()
