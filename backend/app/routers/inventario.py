from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Inventario, CategoriaInventario
from app.schemas.inventario import InventarioCreate, InventarioUpdate, InventarioOut, InventarioListOut
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/inventario", tags=["Inventario"])


@router.get("", response_model=list[InventarioListOut])
def listar_articulos(
    q: str = Query("", description="Búsqueda por nombre, marca o serie"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "inventario.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    query = db.query(Inventario)
    if q:
        query = query.filter(
            or_(
                Inventario.Nombre_Articulo.ilike(f"%{q}%"),
                Inventario.Marca.ilike(f"%{q}%"),
                Inventario.Numero_Serie.ilike(f"%{q}%"),
            )
        )
    articulos = query.order_by(Inventario.Nombre_Articulo).offset(skip).limit(limit).all()

    return [
        InventarioListOut(
            ID_Articulo=a.ID_Articulo,
            Nombre_Articulo=a.Nombre_Articulo,
            Marca=a.Marca,
            Modelo=a.Modelo,
            Numero_Serie=a.Numero_Serie,
            Cantidad=a.Cantidad,
            Estado_Articulo=a.Estado_Articulo,
            Tipo_Ubicacion=a.Tipo_Ubicacion,
            Categoria=a.categoria.Nombre_Categoria if a.categoria else "",
            Iglesia=a.iglesia.Nombre_Iglesia if a.iglesia else "",
        )
        for a in articulos
    ]


@router.get("/{articulo_id}", response_model=InventarioOut)
def obtener_articulo(
    articulo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "inventario.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    art = db.query(Inventario).filter(Inventario.ID_Articulo == articulo_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return art


@router.post("", response_model=InventarioOut, status_code=201)
def crear_articulo(
    data: InventarioCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "inventario.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    art = Inventario(**data.model_dump())
    db.add(art)
    db.commit()
    db.refresh(art)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Inventario", art.ID_Articulo, "Crear inventario")
    db.commit()
    return art


@router.put("/{articulo_id}", response_model=InventarioOut)
def actualizar_articulo(
    articulo_id: int,
    data: InventarioUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "inventario.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    art = db.query(Inventario).filter(Inventario.ID_Articulo == articulo_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(art, key, val)
    db.commit()
    db.refresh(art)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Inventario", art.ID_Articulo, "Actualizar inventario")
    db.commit()
    return art


@router.delete("/{articulo_id}", status_code=204)
def eliminar_articulo(
    articulo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "inventario.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    art = db.query(Inventario).filter(Inventario.ID_Articulo == articulo_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    id_art = art.ID_Articulo
    db.delete(art)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Inventario", id_art, "Eliminar inventario")
    db.commit()
