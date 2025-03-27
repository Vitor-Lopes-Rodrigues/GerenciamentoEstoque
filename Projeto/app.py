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


@app.route("/estoque", methods=["GET", "POST"])
@login_required
def gerenciar_estoque():
    mensagem = None
    if request.method == "POST":
        acao = request.form.get("acao")
        codigo = request.form.get("codigo", "").strip()
        nome = request.form.get("nome", "").strip()
        quantidade_str = request.form.get("quantidade", "").strip()

        # Validação da quantidade
        try:
            quantidade = int(quantidade_str) if quantidade_str else 0
            if quantidade < 0:
                mensagem = "Quantidade não pode ser negativa!"
                return render_template("estoque.html", estoque=estoque, mensagem=mensagem)
        except ValueError:
            mensagem = "Digite uma quantidade válida!"
            return render_template("estoque.html", estoque=estoque, mensagem=mensagem)

        if acao == "cadastrar":
            if codigo in estoque:
                mensagem = "Código já existe!"
            elif not codigo or not nome:
                mensagem = "Código e nome são obrigatórios!"
            else:
                estoque[codigo] = {"nome": nome, "quantidade": quantidade}
                mensagem = f"Produto '{nome}' cadastrado com sucesso!"

        elif acao == "entrada":
            if codigo not in estoque:
                mensagem = "Produto não encontrado!"
            elif quantidade <= 0:
                mensagem = "Quantidade deve ser maior que zero!"
            else:
                estoque[codigo]["quantidade"] += quantidade
                mensagem = f"Entrada registrada! Estoque atual: {estoque[codigo]['quantidade']} unidades"

        elif acao == "saida":
            if codigo not in estoque:
                mensagem = "Produto não encontrado!"
            elif quantidade <= 0:
                mensagem = "Quantidade deve ser maior que zero!"
            elif quantidade > estoque[codigo]["quantidade"]:
                mensagem = f"Estoque insuficiente! Disponível: {estoque[codigo]['quantidade']}"
            else:
                estoque[codigo]["quantidade"] -= quantidade
                mensagem = f"Saída registrada! Estoque atual: {estoque[codigo]['quantidade']} unidades"

    return render_template("estoque.html", estoque=estoque, mensagem=mensagem)



if __name__ == "__main__":
    app.run(debug=True)
