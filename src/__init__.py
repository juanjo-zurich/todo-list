from flask import Flask, render_template
from src import todo, auth
from . import models
from .models import db
def create_app():

    app = Flask(__name__)
    # Configuracion del proyecto
    app.config.from_mapping(
        #DEBUG=True,
        DEBUG=False,
        SECRET_KEY='devtodo',
        SQLALCHEMY_DATABASE_URI="sqlite:///todo_list.db"
        
    )
    db.init_app(app)
    
    #Registrar Blueprint
    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        db.create_all()


    return app

