from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Cliente, Material, Orcamento, OrdemServico

#dashboard_bp = Blueprint('dashboard', __name__)
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# @dashboard_bp.route('/')
# @login_required
# def index():
#     # Estatísticas para o dashboard
#     total_clientes = Cliente.query.count()
#     total_materiais = Material.query.count()
#     orcamentos_pendentes = Orcamento.query.filter_by(status='pendente').count()
#     ordens_em_andamento = OrdemServico.query.filter_by(status='em_andamento').count()
    
#     # Últimos orçamentos
#     ultimos_orcamentos = Orcamento.query.order_by(Orcamento.data_orcamento.desc()).limit(5).all()
    
#     return render_template('dashboard/index.html',
#                          total_clientes=total_clientes,
#                          total_materiais=total_materiais,
#                          orcamentos_pendentes=orcamentos_pendentes,
#                          ordens_em_andamento=ordens_em_andamento,
#                          ultimos_orcamentos=ultimos_orcamentos)
@dashboard_bp.route('/')
@login_required
def index():
    from models import Cliente, Material, Orcamento, OrdemServico, NotaFiscal

    # Contagens simples
    total_clientes = Cliente.query.count()
    total_materiais = Material.query.count()
    total_orcamentos = Orcamento.query.count()
    total_ordens = OrdemServico.query.count()
    orcamentos_pendentes = Orcamento.query.filter_by(status='pendente').count()
    
    # Ordens de serviço por status
    ordens_em_andamento = OrdemServico.query.filter_by(status='em_andamento').count()
    ordens_concluidas = OrdemServico.query.filter_by(status='concluido').count()
    ordens_canceladas = OrdemServico.query.filter_by(status='cancelado').count()

    # Materiais com estoque abaixo do mínimo
    materiais_estoque_baixo = Material.query.filter(Material.quantidade_estoque < Material.estoque_minimo).count()

    # Faturamento: soma dos valores das ordens concluídas
    faturamento_mes = 0.0
    ordens_concluidas_objs = OrdemServico.query.filter_by(status='concluido').all()
    for ordem in ordens_concluidas_objs:
        if ordem.nota_fiscal:
            faturamento_mes += ordem.nota_fiscal.valor_total

    # Últimos orçamentos
    ultimos_orcamentos = Orcamento.query.order_by(Orcamento.data_orcamento.desc()).limit(5).all()

    # Pacote de estatísticas agrupadas
    estatisticas = {
        "total_clientes": total_clientes,
        "total_materiais": total_materiais,
        "total_orcamentos": total_orcamentos,
        "total_ordens": total_ordens,
        "orcamentos_pendentes": orcamentos_pendentes,
        "ordens_em_andamento": ordens_em_andamento,
        "ordens_concluidas": ordens_concluidas,
        "ordens_canceladas": ordens_canceladas,
        "materiais_estoque_baixo": materiais_estoque_baixo,
        "faturamento_mes": faturamento_mes,
    }

    return render_template('dashboard/index.html',
                           estatisticas=estatisticas,
                           ultimos_orcamentos=ultimos_orcamentos)
# Register the blueprint in the main application file
