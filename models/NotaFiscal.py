from extensions import db
from datetime import datetime

class NotaFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey("ordem_servico.id"), unique=True, nullable=False)
    numero_nf = db.Column(db.String(50), unique=True, nullable=False)
    data_emissao = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="emitida") # emitida, cancelada

