from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Miembro
from app.models.usuario import Usuario
from app.utils.security import get_current_user, tiene_permiso

router = APIRouter(prefix="/api/miembros", tags=["Miembros"])


@router.get("/{miembro_id}/profesiones")
def listar_profesiones_miembro(
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return [{"ID": p.ID_Profesion, "Nombre": p.Nombre_Profesion} for p in m.profesiones]


@router.put("/{miembro_id}/profesiones")
def actualizar_profesiones_miembro(
    miembro_id: int,
    data: dict,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    from app.models import Profesion
    ids = data.get("profesiones", [])
    m.profesiones = db.query(Profesion).filter(Profesion.ID_Profesion.in_(ids)).all()
    db.commit()
    return {"mensaje": "Profesiones actualizadas"}


@router.get("/{miembro_id}/oficios")
def listar_oficios_miembro(
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return [{"ID": o.ID_Oficio, "Nombre": o.Nombre_Oficio} for o in m.oficios]


@router.put("/{miembro_id}/oficios")
def actualizar_oficios_miembro(
    miembro_id: int,
    data: dict,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    from app.models import Oficio
    ids = data.get("oficios", [])
    m.oficios = db.query(Oficio).filter(Oficio.ID_Oficio.in_(ids)).all()
    db.commit()
    return {"mensaje": "Oficios actualizados"}
