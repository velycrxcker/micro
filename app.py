from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(20), unique=True, nullable=False)
    contrasena = db.Column(db.String(20), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/usuarios/buscar', methods=['GET'])
def buscar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{ "Id_Usuario": u.id_usuario, "Nombre_Usuario": u.nombre_usuario, "Contrasena": u.contrasena } for u in usuarios])

@app.route('/usuarios/guardar', methods=['POST'])
def guardar_usuario():
    nombre_usuario = request.form['nombre_usuario']
    contrasena = request.form['contrasena']
    nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contrasena=contrasena)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/usuarios/editar', methods=['GET'])
def editar_usuario():
    id_usuario = request.args.get('id_usuario')
    usuario = Usuario.query.get(id_usuario)
    return jsonify([{ "Id_Usuario": usuario.id_usuario, "Nombre_Usuario": usuario.nombre_usuario, "Contrasena": usuario.contrasena }])

@app.route('/usuarios/eliminar', methods=['POST'])
def eliminar_usuario():
    id_usuario = request.form['id_usuario']
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
