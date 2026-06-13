from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# 1. Tabela de Utilizadores (Obrigatória para o Flask-Login - Matéria do Lab 6)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Guardará a password encriptada
    
    # Relações (Cascade garante que se um utilizador apagar a conta, apaga os dados do jogo)
    resources = db.relationship('Resource', backref='user', uselist=False, cascade='all, delete-orphan')
    buildings = db.relationship('BuildingSlot', backref='user', cascade='all, delete-orphan')
    tasks = db.relationship('ActiveTask', backref='user', cascade='all, delete-orphan')

# Função obrigatória do Flask-Login para recuperar o utilizador da sessão (Lab 6)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 2. Tabela de Recursos (Carne e Pedra)
class Resource(db.Model):
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Valores iniciais exigidos pela vossa ideia de projeto
    meat = db.Column(db.Integer, default=50)
    stone = db.Column(db.Integer, default=10)


# 3. Tabela de Slots de Construção (Mecânica de Slots Limitados)
class BuildingSlot(db.Model):
    __tablename__ = 'building_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    slot_number = db.Column(db.Integer, nullable=False) # Ex: Slot 1, Slot 2, Slot 3
    building_type = db.Column(db.String(50), nullable=True) # 'Hunters_Hut', 'Ancestral_Quarry', 'Shaman_Altar' ou None
    status = db.Column(db.String(30), default='Vazio') # 'Vazio', 'Em Construcao', 'Ativo'


# 4. Tabela de Tarefas Temporais (Controlo de Tempo Real Seguro no Servidor)
class ActiveTask(db.Model):
    __tablename__ = 'active_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    task_type = db.Column(db.String(50), nullable=False) # 'Hunt_Mammoth', 'Dig_Spearheads', 'Pintura_Rupestre'
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False) # O carimbo de data/hora em que a tarefa termina no mundo real
    status = db.Column(db.String(30), default='In_Progress') # 'In_Progress', 'Completed_Wait_Collect'