# Rota para a página principal de estoque
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
