from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Cambia esto a tu base de datos
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
    usuarios = Usuario.query.all()
    return render_template('registro.html', usuarios=usuarios)

@app.route('/alumnos/guardar', methods=['POST'])
def guardar_usuario():
    nombre_usuario = request.form['txtNombreUsuario']
    contrasena = request.form['txtContrasena']
    nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contrasena=contrasena)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/alumnos/editar/<int:id_usuario>', methods=['POST'])
def editar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    usuario.nombre_usuario = request.form['txtNombreUsuario']
    usuario.contrasena = request.form['txtContrasena']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/alumnos/eliminar/<int:id_usuario>', methods=['POST'])
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
