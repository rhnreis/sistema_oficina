from main import create_app
from models import Usuario

app = create_app()

with app.app_context():
    usuarios = Usuario.query.all()
    print(f"Total de usuários: {len(usuarios)}")
    for usuario in usuarios:
        print(f"- {usuario.nome} ({usuario.email})")

