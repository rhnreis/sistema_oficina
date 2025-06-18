from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import Usuario
from extensions import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Email ou senha incorretos!', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/cadastrar-usuario', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['password']
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('auth.cadastrar_usuario'))
        
        novo_usuario = Usuario(
            nome=nome,
            email=email
        )
        novo_usuario.set_password(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('auth.listar_usuarios'))
    
    return render_template('auth/cadastrar_usuario.html')

@auth_bp.route('/listar-usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('auth/listar_usuarios.html', usuarios=usuarios)