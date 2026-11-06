from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-sudoku"

# o puzzle é os numeros do sudoku e o solucao é como deve ficar
PUZZLE = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
SOLUCAO = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"

placar = {"Resolvidos": 0}


def novo_jogo():
    session["tabuleiro"] = [int(n) for n in PUZZLE]
    session["selecionada"] = None


def venceu(tabuleiro):
    return tabuleiro == [int(n) for n in SOLUCAO]


@app.route("/")
def index():
    if "tabuleiro" not in session:
        novo_jogo()
    return render_template(
        "index.html",
        tabuleiro=session["tabuleiro"],
        selecionada=session["selecionada"],
        fixas=[n != "0" for n in PUZZLE],
        venceu=venceu(session["tabuleiro"]),
        mensagem=session.pop("mensagem", None),
        placar=placar,
    )


@app.route("/selecionar/<int:posicao>")
def selecionar(posicao):
    tabuleiro = session["tabuleiro"]

    # não deixa selecionar casa fixa nem depois de vencer
    if venceu(tabuleiro) or PUZZLE[posicao] != "0":
        return redirect(url_for("index"))

    session["selecionada"] = posicao
    return redirect(url_for("index"))


@app.route("/colocar/<int:numero>")
def colocar(numero):
    tabuleiro = session["tabuleiro"]
    posicao = session["selecionada"]

    if posicao is None or venceu(tabuleiro) or numero > 9:
        return redirect(url_for("index"))

    tabuleiro[posicao] = numero  # numero 0 apaga a casa
    session["tabuleiro"] = tabuleiro

    if venceu(tabuleiro):
        placar["Resolvidos"] += 1

    return redirect(url_for("index"))


@app.route("/verificar")
def verificar():
    tabuleiro = session["tabuleiro"]
    erros = 0
    for i in range(81):
        if tabuleiro[i] != 0 and tabuleiro[i] != int(SOLUCAO[i]):
            erros += 1

    if erros == 0:
        session["mensagem"] = "Tudo certo até agora!"
    else:
        session["mensagem"] = f"Você tem {erros} número(s) errado(s)."
    return redirect(url_for("index"))


@app.route("/reiniciar")
def reiniciar():
    novo_jogo()
    return redirect(url_for("index"))


@app.route("/regras")
def regras():
    return render_template("regras.html")


if __name__ == "__main__":
    app.run(debug=True)
