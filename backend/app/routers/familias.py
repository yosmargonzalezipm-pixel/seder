from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Familia, Miembro
from app.schemas.familia import FamiliaCreate, FamiliaUpdate, FamiliaOut
from app.utils.security import get_current_user, tiene_permiso
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/familias", tags=["Familias"])


@router.get("", response_model=list[FamiliaOut])
def listar_familias(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Familia)
    if q:
        query = query.filter(Familia.Nombre_Familia.ilike(f"%{q}%"))
    return query.order_by(Familia.Nombre_Familia).all()


@router.get("/{familia_id}", response_model=FamiliaOut)
def obtener_familia(
    familia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    familia = db.query(Familia).filter(Familia.ID_Familia == familia_id).first()
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    return familia


@router.post("", response_model=FamiliaOut, status_code=201)
def crear_familia(
    data: FamiliaCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    familia = Familia(**data.model_dump())
    db.add(familia)
    db.commit()
    db.refresh(familia)
    return familia


@router.put("/{familia_id}", response_model=FamiliaOut)
def actualizar_familia(
    familia_id: int,
    data: FamiliaUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    familia = db.query(Familia).filter(Familia.ID_Familia == familia_id).first()
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(familia, key, val)
    db.commit()
    db.refresh(familia)
    return familia


@router.delete("/{familia_id}", status_code=204)
def eliminar_familia(
    familia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    familia = db.query(Familia).filter(Familia.ID_Familia == familia_id).first()
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    miembros = db.query(Miembro).filter(Miembro.ID_Familia == familia_id).count()
    if miembros > 0:
        raise HTTPException(status_code=400, detail=f"No se puede eliminar: {miembros} miembro(s) pertenecen a esta familia")
    db.delete(familia)
    db.commit()


@router.get("/{familia_id}/miembros")
def miembros_por_familia(
    familia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    miembros = db.query(Miembro).filter(Miembro.ID_Familia == familia_id).all()
    return [
        {"ID_Miembro": m.ID_Miembro, "Cedula": m.Cedula, "Nombres": m.Nombres, "Apellidos": m.Apellidos}
        for m in miembros
    ]
