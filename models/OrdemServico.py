from extensions import db
from datetime import datetime

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey("orcamento.id"), unique=True, nullable=False)
    numero_ordem = db.Column(db.String(50), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_inicio = db.Column(db.DateTime)
    data_conclusao = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="em_andamento") # em_andamento, concluido, cancelado
    observacoes = db.Column(db.Text)

    contrato = db.relationship("Contrato", backref="ordem_servico", uselist=False)
    nota_fiscal = db.relationship("NotaFiscal", backref="ordem_servico", uselist=False)

class ItemOrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey("ordem_servico.id"), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    total_item = db.Column(db.Float, nullable=False)

