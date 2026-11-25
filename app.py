import os
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_login import LoginManager, login_required, current_user
from flask_restful import Api
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed
from models import db, User
import controllers

app = Flask(__name__)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_secreta_muy_segura_12345')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'mysql+pymysql://user:pwd@db/videojuegos'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from api.routes import JuegoList, JuegoResource
api = Api(app, prefix='/api')
api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')

@app.errorhandler(BadRequest)
def handle_400(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(MethodNotAllowed)
def handle_405(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_api_error(e):
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify(code=e.code, name=e.name, description=e.description).data
        response.content_type = 'application/json'
        return response
    return e

@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    lista_juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=lista_juegos)

@app.route("/videogame/<int:id>")
def ver_videojuego(id):
    parametro = request.args.get("ref")
    if not parametro:
        abort(400)
    return f"Videojuego {id} cargado con exito"

@app.route("/error_forzado")
def error_forzado():
    resultado = 1 / 0
    return str(resultado)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for("juegos"))

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id = request.form["id"]
    controllers.eliminar_juego(id)
    return redirect(url_for("juegos"))

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(id, nombre, descripcion, precio)
    return redirect(url_for("juegos"))

def create_app(config_name='default'):
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
    return app


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)