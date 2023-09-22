from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    drogaria_id: int = 1
    texto: str = "Drogaria cadastrada no banco de dados da farmacia popular!"
