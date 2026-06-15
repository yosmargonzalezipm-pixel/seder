from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CategoriaInventario
from app.schemas.profesion_oficio import CatalogoCreate, CatalogoUpdate, CatalogoOut
from app.utils.security import get_current_user, tiene_permiso
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/categorias", tags=["Categorías de Inventario"])


@router.get("", response_model=list[CatalogoOut])
def listar_categorias(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "categorias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(CategoriaInventario)
    if q:
        query = query.filter(CategoriaInventario.Nombre_Categoria.ilike(f"%{q}%"))
    return [CatalogoOut(ID=c.ID_Categoria, Nombre=c.Nombre_Categoria) for c in query.order_by(CategoriaInventario.Nombre_Categoria).all()]


@router.get("/{categoria_id}", response_model=CatalogoOut)
def obtener_categoria(
    categoria_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "categorias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = db.query(CategoriaInventario).filter(CategoriaInventario.ID_Categoria == categoria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return CatalogoOut(ID=c.ID_Categoria, Nombre=c.Nombre_Categoria)


@router.post("", response_model=CatalogoOut, status_code=201)
def crear_categoria(
    data: CatalogoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "categorias.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = CategoriaInventario(Nombre_Categoria=data.Nombre)
    db.add(c)
    db.commit()
    db.refresh(c)
    return CatalogoOut(ID=c.ID_Categoria, Nombre=c.Nombre_Categoria)


@router.put("/{categoria_id}", response_model=CatalogoOut)
def actualizar_categoria(
    categoria_id: int,
    data: CatalogoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "categorias.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = db.query(CategoriaInventario).filter(CategoriaInventario.ID_Categoria == categoria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if data.Nombre is not None:
        c.Nombre_Categoria = data.Nombre
    db.commit()
    db.refresh(c)
    return CatalogoOut(ID=c.ID_Categoria, Nombre=c.Nombre_Categoria)


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(
    categoria_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "categorias.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = db.query(CategoriaInventario).filter(CategoriaInventario.ID_Categoria == categoria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(c)
    db.commit()
