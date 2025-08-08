from flask import Flask
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import Usuario
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.clientes import clientes_bp
    from routes.dashboard import dashboard_bp
    from routes.materiais import materiais_bp    
    from routes.notas_fiscais import notas_fiscais_bp
    from routes.orcamentos import orcamentos_bp
    from routes.ordens import ordens_bp
    from routes.relatorios import relatorios_bp
    from routes.configuracoes import configuracoes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(materiais_bp)
    app.register_blueprint(notas_fiscais_bp)
    app.register_blueprint(orcamentos_bp)
    app.register_blueprint(ordens_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(configuracoes_bp)


    # ... outros blueprints
    
    # Criar usuário inicial se não existir
    with app.app_context():
        from models import Usuario
        if not Usuario.query.filter_by(email='rodrigo@lantercar.com').first():
            admin = Usuario(
                nome='Rodrigo',
                email='rodrigo@lantercar.com'
            )
            admin.set_password('1234')
            db.session.add(admin)
            db.session.commit()
    
    return app
 #rodrigo@lantercar.com / 1234
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
