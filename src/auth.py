import functools
from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .models import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registro', methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, generate_password_hash(password))
        error = None

        user_name = User.query.filter_by(username= username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario: {username}, ya existe en la base de datos.'
            flash(error)
    return render_template('auth/registro.html')

@bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        print(f'Error: {error}')
        # Validar datos
        user = User.query.filter_by(username=username).first()

        if user == None:
            error = f'El usuario no existe en la base de datos.'

        elif not check_password_hash(user.password, password):
            error = f'La contraseña es incorrecta.'


        # Iniciar session
        if error == None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.listar'))

        flash(error)
    return  render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_user():
    user_id = session.get('user_id')

    if user_id == None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
        print(f'g.user: {g.user.id}')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

