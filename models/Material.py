from extensions import db

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    estoque = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)
    unidade_medida = db.Column(db.String(10), default='UN')
    valor_frete = db.Column(db.Float, nullable=True)  # Valor do frete calculado na criação
    codigo_gerado = db.Column(db.Boolean, default=False)  # Indica se o código foi gerado automaticamente

    itens_orcamento = db.relationship('ItemOrcamento', backref='material', lazy=True)

