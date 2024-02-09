import datetime
from flask import Flask, request
from database import save_objeto, get_session
from models import Transacao, Cliente

app = Flask(__name__)

session = get_session()

@app.route("/clientes/<cliente_id>/transacoes", methods=["POST"])
def create_transacao(cliente_id):
    cliente = session.query(Cliente).filter_by(id=cliente_id).first()
    if not cliente:
        return {"error":"cliente não encontrado."},404
    
    dados = request.get_json()
    valor = dados["valor"]
    tipo = dados["tipo"]
    descricao = dados["descricao"]

    if tipo == 'd':
        try:
            cliente.debitar(valor)
        except Exception as e:
            return {"error": "{}".format(e)}, 422
    else:
        cliente.creditar(valor)
    
    nova_transacao = Transacao(valor, tipo, descricao, cliente_id)
    save_objeto(nova_transacao, session)

    return {"limite": cliente.get_limite(),
            "saldo" : cliente.get_saldo()},200


@app.route("/clientes/<cliente_id>/extrato", methods= ["GET"])
def get_transacoes(cliente_id):
    cliente = session.query(Cliente).filter_by(id=cliente_id).first()
    if not cliente:
        return {"error":"cliente não encontrado."},404
    
    transacoes = session.query(Transacao).filter_by(cliente_id=cliente_id).order_by(Transacao.realizada_em.desc()).limit(10).all()
    
    extrato = {"saldo": {
        "total": cliente.get_saldo(),
        "data_extrato": str(datetime.datetime.utcnow()),
        "limite" : cliente.get_limite()
    },
        "ultimas_transacoes": [transacao.to_dict() for transacao in transacoes]}

    return extrato, 200


if __name__ == "__main__":
    app.run("0.0.0.0" , port=5000)