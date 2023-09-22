from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Drogaria(Base):
    __tablename__ = 'drogaria'

    id = Column("pk_drogaria", Integer, primary_key=True)
    nome_drogaria = Column(String(140), unique=True)
    nome_responsavel = Column(String(100))
    crf = Column(Integer)
    endereco = Column(String)
    telefone = Column(String(15))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a drogaria e o comentário.
    # Essa relação é implicita, não está salva na tabela 'drogaria',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome_drogaria:str, nome_responsavel:str, crf:int, endereco:str,telefone:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Drogaria

        Arguments:
            nome: nome da drogaria.
            nome do responsavel tecnico: Farmaceutico responsavel pela drogaria
            Crf: Registro do farmaceutico
            endereço: endereço da drogaria
            telefone: telefone da mesma
            data_insercao: data de quando a drogaria foi inserida à base
        """
        self.nome_drogaria = nome_drogaria
        self.nome_responsavel = nome_responsavel
        self.crf = crf
        self.endereco = endereco
        self.telefone = telefone

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Drogaria
        """
        self.comentarios.append(comentario)

