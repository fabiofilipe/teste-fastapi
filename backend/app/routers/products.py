"""Router para gerenciamento de produtos do cardápio"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.models import Produto, Usuario, ProdutoVariacao, ProdutoIngrediente, Categoria, Ingrediente
from app.schemas.schemas import (
    ProdutoCreate, ProdutoUpdate, ProdutoResponse,
    ProdutoVariacaoCreate, ProdutoVariacaoUpdate, ProdutoVariacaoResponse
)
from app.dependencies.auth import obter_usuario_admin
from app.exceptions import (
    ProdutoNaoEncontrado, CategoriaNaoEncontrada,
    IngredienteNaoEncontrado, ProdutoVariacaoNaoEncontrada
)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Cria um novo produto no cardápio com variações e ingredientes"""
    # Verificar se categoria existe
    categoria = db.query(Categoria).filter(Categoria.id == produto.categoria_id).first()
    if not categoria:
        raise CategoriaNaoEncontrada(produto.categoria_id)

    # Verificar se produto com mesmo nome já existe
    produto_existente = db.query(Produto).filter(Produto.nome == produto.nome).first()
    if produto_existente:
        from app.exceptions import PizzariaException
        raise PizzariaException(f"Produto '{produto.nome}' já existe", status.HTTP_400_BAD_REQUEST)

    # Criar novo produto
    novo_produto = Produto(
        categoria_id=produto.categoria_id,
        nome=produto.nome,
        descricao=produto.descricao,
        imagem_url=produto.imagem_url,
        disponivel=produto.disponivel
    )
    db.add(novo_produto)
    db.flush()  # Para obter o ID do produto

    # Criar variações
    for variacao_data in produto.variacoes:
        variacao = ProdutoVariacao(
            produto_id=novo_produto.id,
            tamanho=variacao_data.tamanho,
            preco=variacao_data.preco,
            disponivel=variacao_data.disponivel
        )
        db.add(variacao)

    # Adicionar ingredientes padrão
    for ingrediente_id in produto.ingredientes_ids:
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            raise IngredienteNaoEncontrado(ingrediente_id)

        produto_ingrediente = ProdutoIngrediente(
            produto_id=novo_produto.id,
            ingrediente_id=ingrediente_id
        )
        db.add(produto_ingrediente)

    db.commit()
    db.refresh(novo_produto)

    # Carregar relacionamentos
    produto_completo = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))\
        .filter(Produto.id == novo_produto.id)\
        .first()

    return produto_completo


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    disponivel: bool = None,
    categoria_id: int = None,
    db: Session = Depends(get_db)
):
    """Lista todos os produtos do cardápio com filtros opcionais"""
    query = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))

    # Aplicar filtros
    if disponivel is not None:
        query = query.filter(Produto.disponivel == disponivel)

    if categoria_id:
        query = query.filter(Produto.categoria_id == categoria_id)

    produtos = query.all()
    return produtos


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Busca um produto específico por ID"""
    produto = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))\
        .filter(Produto.id == produto_id)\
        .first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Atualiza um produto existente"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    # Verificar categoria se fornecida
    update_data = produto_update.model_dump(exclude_unset=True)
    if 'categoria_id' in update_data:
        categoria = db.query(Categoria).filter(Categoria.id == update_data['categoria_id']).first()
        if not categoria:
            raise CategoriaNaoEncontrada(update_data['categoria_id'])

    # Atualizar campos
    for campo, valor in update_data.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    # Carregar relacionamentos
    produto_completo = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))\
        .filter(Produto.id == produto_id)\
        .first()

    return produto_completo


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Remove um produto do cardápio"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    db.delete(produto)
    db.commit()

    return None


@router.patch("/{produto_id}/disponibilidade", response_model=ProdutoResponse)
def alternar_disponibilidade(
    produto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Alterna a disponibilidade de um produto"""
    produto = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))\
        .filter(Produto.id == produto_id)\
        .first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    produto.disponivel = not produto.disponivel
    db.commit()
    db.refresh(produto)

    return produto


# Endpoints para gerenciar variações
@router.post("/{produto_id}/variacoes", response_model=ProdutoVariacaoResponse, status_code=status.HTTP_201_CREATED)
def adicionar_variacao(
    produto_id: int,
    variacao: ProdutoVariacaoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Adiciona uma nova variação a um produto"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    # Verificar se variação com mesmo tamanho já existe
    variacao_existente = db.query(ProdutoVariacao).filter(
        ProdutoVariacao.produto_id == produto_id,
        ProdutoVariacao.tamanho == variacao.tamanho
    ).first()

    if variacao_existente:
        from app.exceptions import PizzariaException
        raise PizzariaException(
            f"Variação '{variacao.tamanho}' já existe para este produto",
            status.HTTP_400_BAD_REQUEST
        )

    nova_variacao = ProdutoVariacao(
        produto_id=produto_id,
        **variacao.model_dump()
    )
    db.add(nova_variacao)
    db.commit()
    db.refresh(nova_variacao)

    return nova_variacao


@router.put("/{produto_id}/variacoes/{variacao_id}", response_model=ProdutoVariacaoResponse)
def atualizar_variacao(
    produto_id: int,
    variacao_id: int,
    variacao_update: ProdutoVariacaoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Atualiza uma variação existente"""
    variacao = db.query(ProdutoVariacao).filter(
        ProdutoVariacao.id == variacao_id,
        ProdutoVariacao.produto_id == produto_id
    ).first()

    if not variacao:
        raise ProdutoVariacaoNaoEncontrada(variacao_id)

    update_data = variacao_update.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(variacao, campo, valor)

    db.commit()
    db.refresh(variacao)

    return variacao


@router.delete("/{produto_id}/variacoes/{variacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_variacao(
    produto_id: int,
    variacao_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Deleta uma variação de produto"""
    variacao = db.query(ProdutoVariacao).filter(
        ProdutoVariacao.id == variacao_id,
        ProdutoVariacao.produto_id == produto_id
    ).first()

    if not variacao:
        raise ProdutoVariacaoNaoEncontrada(variacao_id)

    db.delete(variacao)
    db.commit()

    return None


# Endpoints para gerenciar ingredientes padrão
@router.post("/{produto_id}/ingredientes/{ingrediente_id}", status_code=status.HTTP_201_CREATED)
def adicionar_ingrediente_padrao(
    produto_id: int,
    ingrediente_id: int,
    obrigatorio: bool = False,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Adiciona um ingrediente padrão a um produto"""
    # Verificar se produto existe
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    # Verificar se ingrediente existe
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise IngredienteNaoEncontrado(ingrediente_id)

    # Verificar se já existe
    existente = db.query(ProdutoIngrediente).filter(
        ProdutoIngrediente.produto_id == produto_id,
        ProdutoIngrediente.ingrediente_id == ingrediente_id
    ).first()

    if existente:
        from app.exceptions import PizzariaException
        raise PizzariaException(
            f"Ingrediente '{ingrediente.nome}' já está associado a este produto",
            status.HTTP_400_BAD_REQUEST
        )

    produto_ingrediente = ProdutoIngrediente(
        produto_id=produto_id,
        ingrediente_id=ingrediente_id,
        obrigatorio=obrigatorio
    )
    db.add(produto_ingrediente)
    db.commit()

    return {"message": f"Ingrediente '{ingrediente.nome}' adicionado ao produto"}


@router.delete("/{produto_id}/ingredientes/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_ingrediente_padrao(
    produto_id: int,
    ingrediente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Remove um ingrediente padrão de um produto"""
    produto_ingrediente = db.query(ProdutoIngrediente).filter(
        ProdutoIngrediente.produto_id == produto_id,
        ProdutoIngrediente.ingrediente_id == ingrediente_id
    ).first()

    if not produto_ingrediente:
        from app.exceptions import PizzariaException
        raise PizzariaException(
            "Ingrediente não está associado a este produto",
            status.HTTP_404_NOT_FOUND
        )

    db.delete(produto_ingrediente)
    db.commit()

    return None
