
from extensions import db
from datetime import datetime

class Configuracao(db.Model):
    __tablename__ = 'configuracoes'
    id = db.Column(db.Integer, primary_key=True)
    fator_divisao = db.Column(db.Float, nullable=False, default=1.0)
    porcentagem_frete = db.Column(db.Float, nullable=False, default=0.0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Configuracao {self.id}>'
