from extensions import db
from datetime import datetime, date

class Orcamento(db.Model):
    ordens_servico = db.relationship("OrdemServico", back_populates="orcamento")
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    numero_orcamento = db.Column(db.String(50), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_orcamento = db.Column(db.DateTime, default=datetime.utcnow)
    descricao_servico = db.Column(db.Text, nullable=False)
    valor_mao_obra = db.Column(db.Float, default=0.0)
    valor_total = db.Column(db.Float, default=0.0)
    validade = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(50), default="pendente") # pendente, aceito, rejeitado

    itens = db.relationship("ItemOrcamento", backref="orcamento", lazy=True)
    ordem_servico = db.relationship("OrdemServico", back_populates="orcamento", uselist=False)
    cliente = db.relationship("Cliente", back_populates="orcamentos")
    
    def calcular_total(self):
        total_materiais = sum(item.total_item for item in self.itens)
        self.valor_total = total_materiais + (self.valor_mao_obra or 0)

class ItemOrcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey("orcamento.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"))
    descricao = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    total_item = db.Column(db.Float, nullable=False)
    
    def calcular_subtotal(self):
        self.total_item = self.quantidade * self.preco_unitario

