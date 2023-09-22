from pydantic import BaseModel
from typing import Optional, List
from model.drogaria import Drogaria

from schemas import ComentarioSchema


class DrogariaSchema(BaseModel):
    """ Define como uma nova drogaria a ser inserida deve ser representada
    """
    nome_drogaria: str = "Venancio"
    nome_responsavel: str = "Maria das Dores"
    crf: int = 12345
    endereco: str = "Av. Olegário Maciel, 188"
    telefone: str = "(21) 3095-1000"


class DrogariaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da drogaria.
    """
    nome_drogaria: str = "Drogaria Teste"


class ListagemDrogariasSchema(BaseModel):
    """ Define como uma listagem de drogaria será retornada.
    """
    drogarias:List[DrogariaSchema]


def apresenta_drogarias(drogarias: List[Drogaria]):
    """ Retorna uma representação da drogaria seguindo o schema definido em
        DrogariaViewSchema.
    """
    result = []
    for drogaria in drogarias:
        result.append({
            "nome_drogaria": drogaria.nome_drogaria,
            "nome_responsavel": drogaria.nome_responsavel,
            "crf": drogaria.crf,
            "endereco": drogaria.endereco,
            "telefone": drogaria.telefone,
        })

    return {"drogarias": result}


class DrogariaViewSchema(BaseModel):
    """ Define como uma drogaria será retornado: drogaria + comentários.
    """
    id: int = 1
    nome_drogaria: str = "Venancio"
    nome_responsavel: str = "Maria das Dores"
    crf: int = 12345
    endereco: str = "Av. Olegário Maciel, 188"
    telefone: str = "(21) 3095-1000"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class DrogariaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_drogaria: str

def apresenta_drogaria(drogaria: Drogaria):
    """ Retorna uma representação da drogaria seguindo o schema definido em
        DrogariaViewSchema.
    """
    return {
        "id": drogaria.id,
        "nome_drogaria": drogaria.nome_drogaria,
        "nome_responsavel": drogaria.nome_responsavel,
        "crf": drogaria.crf,
        "endereco": drogaria.endereco,
        "telefone": drogaria.telefone,
        "total_cometarios": len(drogaria.comentarios),
        "comentarios": [{"texto": c.texto} for c in drogaria.comentarios]
    }
