from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    limite = Column(Integer, nullable=False)
   
    def __init__(self, limite):
        self.limite = limite

    def get_limite(self):
        return self.limite
    
    
class Saldo(Base):
    __tablename__ = 'saldos'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    valor = Column(Integer, nullable=False)

    def get_valor(self):
        return self.valor

    def debitar(self, valor_debito, limite):
        if (self.valor - valor_debito < -limite):
            raise ValueError("Débito excede o limite disponível.")
        self.valor -= valor_debito
        return self.valor
        
    def creditar(self, valor):
        self.valor += valor
        return self.valor


class Transacao(Base):
    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True)
    valor = Column(Integer, nullable=False)
    tipo = Column(String(1), nullable=False)
    descricao = Column(String(10), nullable=False)
    realizada_em = Column(DateTime, nullable=False, server_default=func.now())
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)

    def __init__(self, valor, tipo, descricao, cliente_id):
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao
        self.cliente_id = cliente_id

    def to_dict(self):
        return {
            'valor': self.valor,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'realizada_em': self.realizada_em.isoformat(),
        }