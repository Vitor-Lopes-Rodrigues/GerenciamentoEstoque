from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_secreta_123"

# Dicionário para armazenar o estoque (em memória)
estoque = {}

# Credenciais fixas para o login
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Decorador para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("Por favor, faça login primeiro!")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Rota para a página de login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            session["logged_in"] = True
            return redirect(url_for("gerenciar_estoque"))
        else:
            flash("Usuário ou senha incorretos!")
    return render_template("login.html")


# Rota para logout
@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("Você saiu com sucesso!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)