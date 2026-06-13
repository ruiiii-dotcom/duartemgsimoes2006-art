from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'chave_secreta_projeto_daw'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tribo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ... (código inicial igual) ...
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Ajusta esta secção final com muita atenção à indentação (espaços):
    with app.app_context():
        # Importamos os modelos para o SQLAlchemy saber que as tabelas existem
        from app import models 
        db.create_all() # Cria o ficheiro 'tribo.db' com todas as tabelas estruturadas

        # Importamos e registamos a rota inicial
        from app.controllers.main import main_bp
        app.register_blueprint(main_bp)
        
        from app.controllers.auth import auth_bp
        app.register_blueprint(auth_bp)

        from app.controllers.game import game_bp
        app.register_blueprint(game_bp)

    return app