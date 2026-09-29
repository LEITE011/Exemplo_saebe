from flask import Flask, render_template,request, url_for, redirect, flash
from sqlalchemy import select
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import Usuario, Produto, Movimentacao, db_session
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta'

#configuração flask login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para acessar o sistema'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['form_email']
    senha = request.form['form_senha']
    if not email:
        flash('Campo email vazio é obrigatorio', 'danger')
        return render_template('login.html')
    if not senha:
        flash('Campo senha vazio é obrigatorio', 'danger')
        return render_template('login.html')

    usuario = db_session.execute(select(Usuario).where(Usuario.email == email)).scalar()
    if usuario and usuario.check_password(senha):
        login_user(usuario)
        return redirect(url_for('dashboard'))
    else:
        flash('Falha na autenticação: E-mail ou senha incorretos.', 'danger')
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, port=5006)

