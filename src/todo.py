
from flask import Blueprint, render_template, request, redirect, url_for, g
from src.auth import login_required
from .models import Todo, User, db




bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/listar')
@login_required
def listar():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos=todos)

@bp.route('/crear', methods=['POST', 'GET'])
@login_required
def crear():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(g.user.id, title, desc)
        print(f'tdo: {todo}')
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.listar'))
    return render_template('todo/crear.html')

def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo
    
@bp.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
    todo = get_todo(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False

        todo = Todo(g.user.id, todo.title, todo.desc)
        print(f'todo_actualizado: {todo}')
       
        db.session.commit()
        return redirect(url_for('todo.listar'))
    
    
    return render_template('todo/update.html', todo=todo)

@bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    todo = get_todo(id)
    print(todo)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.listar'))

