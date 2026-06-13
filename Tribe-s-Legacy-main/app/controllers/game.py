from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import ActiveTask, Resource
from datetime import datetime, timedelta

# Criamos o Blueprint para as mecânicas do jogo
game_bp = Blueprint('game', __name__)

@game_bp.route('/api/iniciar_cacada', methods=['POST'])
@login_required
def iniciar_cacada():
    # 1. Verifica se o jogador já tem uma caçada em curso
    tarefa_existente = ActiveTask.query.filter_by(user_id=current_user.id, task_type='Caçar Mamute').first()
    if tarefa_existente:
        return jsonify({"sucesso": False, "mensagem": "Os teus caçadores já estão ocupados!"})

    # 2. Define o tempo: A hora atual do servidor + 10 segundos
    agora = datetime.utcnow()
    fim = agora + timedelta(seconds=10)
    
    # 3. Regista a tarefa na Base de Dados para evitar "batoteiros"
    nova_tarefa = ActiveTask(
        user_id=current_user.id,
        task_type='Caçar Mamute',
        start_time=agora,
        end_time=fim,
        status='In_Progress'
    )
    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify({"sucesso": True, "mensagem": "Caçada iniciada! Os caçadores voltam em 10 segundos."})

@game_bp.route('/api/recolher_cacada', methods=['POST'])
@login_required
def recolher_cacada():
    # 1. Procura a tarefa na base de dados
    tarefa = ActiveTask.query.filter_by(user_id=current_user.id, task_type='Caçar Mamute').first()
    
    if not tarefa:
        return jsonify({"sucesso": False, "mensagem": "Não tens nenhuma caçada pronta a recolher."})
        
    # 2. Validação de Segurança: Confirma no servidor se os 10 segundos já passaram mesmo
    if datetime.utcnow() < tarefa.end_time:
        return jsonify({"sucesso": False, "mensagem": "Calma, os caçadores ainda não voltaram!"})
        
    # 3. Sucesso! Damos +20 de Carne ao utilizador
    recursos = Resource.query.filter_by(user_id=current_user.id).first()
    recursos.meat += 20
    
    # 4. Apagamos a tarefa concluída da Base de Dados
    db.session.delete(tarefa)
    db.session.commit()
    
    return jsonify({
        "sucesso": True, 
        "mensagem": "Recolheste 20 de Carne com sucesso!",
        "nova_carne": recursos.meat
    })