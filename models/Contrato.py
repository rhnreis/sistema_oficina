from extensions import db
from datetime import datetime

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey("ordem_servico.id"), unique=True, nullable=False)
    numero_contrato = db.Column(db.String(50), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    termos_condicoes = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="ativo") # ativo, cancelado

