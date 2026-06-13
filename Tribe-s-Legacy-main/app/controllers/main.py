from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Resource

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required # Obriga o jogador a fazer login. Se não tiver, o Flask manda-o para a página de login
def index():
    # Vai à Base de Dados buscar os recursos específicos de quem fez o login
    recursos = Resource.query.filter_by(user_id=current_user.id).first()
    
    # Envia o HTML, mas agora "injetamos" os dados do utilizador lá para dentro
    return render_template('index.html', user=current_user, recursos=recursos)