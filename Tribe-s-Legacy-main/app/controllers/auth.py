from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User, Resource
from app import db

# Criar o Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registo', methods=['GET', 'POST'])
def register():
    # Se o utilizador clicou no botão "Registar" do formulário (POST)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar se já existe alguém com este nome
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return "Erro: Esse nome de chefe de tribo já está a ser usado!"

        # Encriptar a password por segurança (Requisito da disciplina)
        hashed_password = generate_password_hash(password)
        
        # 1. Criar o Utilizador
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit() # Guardamos para ele receber um ID na Base de Dados

        # 2. Criar os recursos iniciais para este novo utilizador (50 Carne, 10 Pedra)
        new_resources = Resource(user_id=new_user.id, meat=50, stone=10)
        db.session.add(new_resources)
        db.session.commit()

        # Depois de registar, reencaminha para a página de login
        return redirect(url_for('auth.login'))
        
    # Se ele apenas acedeu à página (GET), mostra o HTML do formulário
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Verifica se o utilizador existe e se a password está correta
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index')) # Se o login der certo, vai para o Jogo
        else:
            return "Erro: Nome ou password incorretos!"
            
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required # Só quem está com login feito pode fazer logout
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

