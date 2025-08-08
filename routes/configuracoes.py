from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Configuracao

configuracoes_bp = Blueprint('configuracoes', __name__, url_prefix='/configuracoes')

@configuracoes_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Redireciona para o painel por padrão."""
    return redirect(url_for('configuracoes.painel'))

@configuracoes_bp.route('/painel', methods=['GET', 'POST'])
@login_required
def painel():
    config = Configuracao.query.order_by(Configuracao.id.desc()).first()
    if request.method == 'POST':
        fator_divisao = float(request.form.get('fator_divisao', 1.0))
        porcentagem_frete = float(request.form.get('porcentagem_frete', 0.0))
        if config:
            config.fator_divisao = fator_divisao
            config.porcentagem_frete = porcentagem_frete
        else:
            config = Configuracao(fator_divisao=fator_divisao, porcentagem_frete=porcentagem_frete)
            db.session.add(config)
        db.session.commit()
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('configuracoes.painel'))
    return render_template('configuracoes/painel.html', config=config)