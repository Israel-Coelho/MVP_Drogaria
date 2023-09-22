from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Drogaria, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
drogaria_tag = Tag(name="Drogaria", description="Adição, visualização e remoção de drogarias à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à uma drogaria cadastrada na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/drogaria', tags=[drogaria_tag],
          responses={"200": DrogariaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_drogaria(form: DrogariaSchema):
    """Adiciona uma nova Drogaria à base de dados

    Retorna uma representação das drogarias e comentários associados.
    """
    drogaria = Drogaria(
        nome_drogaria=form.nome_drogaria,
        nome_responsavel=form.nome_responsavel,
        crf=form.crf,
        endereco=form.endereco,
        telefone=form.telefone)
    logger.debug(f"Adicionando drogaria de nome: '{drogaria.nome_drogaria}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando drogaria
        session.add(drogaria)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado drogaria de nome: '{drogaria.nome_drogaria}'")
        return apresenta_drogaria(drogaria), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Drogaria de mesmo nome já salvo na base de dados"
        logger.warning(f"Erro ao adicionar drogaria '{drogaria.nome_drogaria}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova drogaria"
        logger.warning(f"Erro ao adicionar drogaria '{drogaria.nome_drogaria}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/drogarias', tags=[drogaria_tag],
         responses={"200": ListagemDrogariasSchema, "404": ErrorSchema})
def get_drogarias():
    """Faz a busca por todos as Drogarias cadastradas

    Retorna uma representação da listagem de drogarias.
    """
    logger.debug(f"Coletando drogaria ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    drogarias = session.query(Drogaria).all()

    if not drogarias:
        # se não há drogarias cadastradas
        return {"drogarias": []}, 200
    else:
        logger.debug(f"%d drogarias econtradas" % len(drogarias))
        # retorna a representação de drogaria
        print(drogarias)
        return apresenta_drogarias(drogarias), 200


@app.get('/drogaria', tags=[drogaria_tag],
         responses={"200": DrogariaViewSchema, "404": ErrorSchema})
def get_drogaria(query: DrogariaBuscaSchema):
    """Faz a busca por uma Drogaria a partir do id da drogaria

    Retorna uma representação das drogarias e comentários associados.
    """
    drogaria_id = query.id
    logger.debug(f"Coletando dados sobre drogaria #{drogaria_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    drogaria = session.query(Drogaria).filter(Drogaria.id == drogaria_id).first()

    if not drogaria:
        # se a drogaria não foi encontrada
        error_msg = "Drogaria não encontrada na base de dados"
        logger.warning(f"Erro ao buscar drogaria '{drogaria_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Drogaria econtrada: '{drogaria.nome_drogaria}'")
        # retorna a representação de drogaria
        return apresenta_drogaria(drogaria), 200


@app.delete('/drogaria', tags=[drogaria_tag],
            responses={"200": DrogariaDelSchema, "404": ErrorSchema})
def del_drogaria(query: DrogariaBuscaSchema):
    """Deleta uma Drogaria a partir do nome da mesma informado

    Retorna uma mensagem de confirmação da remoção.
    """
    drogaria_nome_drogaria = unquote(unquote(query.nome_drogaria))
    print(drogaria_nome_drogaria)
    logger.debug(f"Deletando dados sobre drogaria #{drogaria_nome_drogaria}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Drogaria).filter(Drogaria.nome_drogaria == drogaria_nome_drogaria).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado drogaria #{drogaria_nome_drogaria}")
        return {"mesage": "Drogaria removida", "id": drogaria_nome_drogaria}
    else:
        # se a drogaria não foi encontrada
        error_msg = "Drogaria não encontrado na base de dados"
        logger.warning(f"Erro ao deletar drogaria #'{drogaria_nome_drogaria}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": DrogariaViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à uma drogaria cadastrada na base identificado pelo id

    Retorna uma representação das drogarias e comentários associados.
    """
    drogaria_id  = form.drogaria_id
    logger.debug(f"Adicionando comentários a drogaria #{drogaria_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pela drogaria
    drogaria = session.query(Drogaria).filter(Drogaria.id == drogaria_id).first()

    if not drogaria:
        # se drogaria não encontrada
        error_msg = "Drogaria não encontrada na base de dados"
        logger.warning(f"Erro ao adicionar comentário a drogaria '{drogaria_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário a drogaria
    drogaria.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário a drogaria #{drogaria_id}")

    # retorna a representação da drogaria
    return apresenta_drogaria(drogaria), 200
