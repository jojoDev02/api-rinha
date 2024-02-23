import datetime
from flask import Flask, request
from database import save_objeto, get_session
from models import Transacao, Cliente, Saldo

app = Flask(__name__)

session = get_session()

def get_saldo_by_cliente_id(cliente_id_buscado):
    saldo = session.query(Saldo).filter_by(cliente_id = cliente_id_buscado).first()
    return saldo

def get_cliente_by_id(cliente_id):
   cliente = session.query(Cliente).filter_by(id=cliente_id).first()
   return cliente

@app.route("/clientes/<cliente_id>/transacoes", methods=["POST"])
def create_transacao(cliente_id):
    cliente = get_cliente_by_id(cliente_id)

    if not cliente:
        return {"error":"cliente não encontrado."},404
    
    dados = request.get_json()
    valor = dados["valor"]
    tipo = dados["tipo"]
    descricao = dados["descricao"]
    
    if tipo != 'c' and tipo != 'd' or descricao is None or len(descricao) < 1 or len(descricao) > 10:
        return {"error": "Dados inválidos."}, 422
    
    saldo = get_saldo_by_cliente_id(cliente_id) 

    if tipo == 'd':
        limite = cliente.get_limite()
        try:
            saldo_atualizado = saldo.debitar(valor, limite)
        except Exception as e:
            return {"error": "{}".format(e)}, 422
    elif tipo == 'c':
        saldo_atualizado = saldo.creditar(valor)
        
    
    nova_transacao = Transacao(valor, tipo, descricao, cliente_id)
    session.add(nova_transacao)
    # save_objeto(nova_transacao, session)

    return {"limite": cliente.get_limite(),
            "saldo" : saldo_atualizado},200


@app.route("/clientes/<cliente_id>/extrato", methods= ["GET"])
def get_transacoes(cliente_id):
    cliente = get_cliente_by_id(cliente_id)
    if not cliente:
        return {"error":"cliente não encontrado."},404
    
    saldo = get_saldo_by_cliente_id(cliente_id)
    transacoes = session.query(Transacao).filter_by(cliente_id=cliente_id).order_by(Transacao.realizada_em.desc()).limit(10).all()
    
    extrato = {"saldo": {
        "total": saldo.get_valor(),
        "data_extrato": str(datetime.datetime.utcnow()),
        "limite" : cliente.get_limite()
    },
        "ultimas_transacoes": [transacao.to_dict() for transacao in transacoes]}

    return extrato, 200


if __name__ == "__main__":
    app.run("0.0.0.0" , port=5000, debug=False)