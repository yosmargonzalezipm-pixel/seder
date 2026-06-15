from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Miembro, Iglesia, Profesion, Oficio
from app.schemas.miembro import MiembroCreate, MiembroUpdate, MiembroOut, MiembroListOut
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/miembros", tags=["Miembros"])


@router.get("", response_model=list[MiembroListOut])
def listar_miembros(
    q: str = Query("", description="Búsqueda por cédula, nombres o apellidos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    query = db.query(Miembro)
    if q:
        query = query.filter(
            or_(
                Miembro.Cedula.ilike(f"%{q}%"),
                Miembro.Nombres.ilike(f"%{q}%"),
                Miembro.Apellidos.ilike(f"%{q}%"),
            )
        )
    total = query.count()
    miembros = query.order_by(Miembro.Apellidos).offset(skip).limit(limit).all()

    return [
        MiembroListOut(
            ID_Miembro=m.ID_Miembro,
            Cedula=m.Cedula,
            Nombres=m.Nombres,
            Apellidos=m.Apellidos,
            Telefono=m.Telefono,
            Correo_Electronico=m.Correo_Electronico,
            Sexo=m.Sexo,
            Estado_Civil=m.Estado_Civil,
            Fecha_Nacimiento=m.Fecha_Nacimiento,
            Estado=m.Estado,
            Iglesia=m.iglesia.Nombre_Iglesia if m.iglesia else "",
            Profesiones=[p.Nombre_Profesion for p in m.profesiones],
            Oficios=[o.Nombre_Oficio for o in m.oficios],
        )
        for m in miembros
    ]


@router.get("/{miembro_id}", response_model=MiembroOut)
def obtener_miembro(
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return MiembroOut(
        ID_Miembro=miembro.ID_Miembro,
        ID_Iglesia=miembro.ID_Iglesia,
        Cedula=miembro.Cedula,
        Nombres=miembro.Nombres,
        Apellidos=miembro.Apellidos,
        Fecha_Nacimiento=miembro.Fecha_Nacimiento,
        Telefono=miembro.Telefono,
        Correo_Electronico=miembro.Correo_Electronico,
        Fecha_Bautismo=miembro.Fecha_Bautismo,
        Fecha_Conversion=miembro.Fecha_Conversion,
        Estado=miembro.Estado,
        ID_Familia=miembro.ID_Familia,
        ID_Ciudad=miembro.ID_Ciudad,
        ID_Parroquia=miembro.ID_Parroquia,
        Direccion=miembro.Direccion,
        Sexo=miembro.Sexo,
        Estado_Civil=miembro.Estado_Civil,
        Profesiones=[p.Nombre_Profesion for p in miembro.profesiones],
        Oficios=[o.Nombre_Oficio for o in miembro.oficios],
    )


@router.post("", response_model=MiembroOut, status_code=201)
def crear_miembro(
    data: MiembroCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    existe = db.query(Miembro).filter(Miembro.Cedula == data.Cedula).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un miembro con esa cédula")

    miembro = Miembro(**data.model_dump())
    db.add(miembro)
    db.commit()
    db.refresh(miembro)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Miembros", miembro.ID_Miembro, "Crear miembro")
    db.commit()
    return miembro


@router.put("/{miembro_id}", response_model=MiembroOut)
def actualizar_miembro(
    miembro_id: int,
    data: MiembroUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(miembro, key, val)
    db.commit()
    db.refresh(miembro)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Miembros", miembro.ID_Miembro, "Actualizar miembro")
    db.commit()
    return miembro


@router.delete("/{miembro_id}", status_code=204)
def eliminar_miembro(
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "miembros.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")

    id_miembro = miembro.ID_Miembro
    db.delete(miembro)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Miembros", id_miembro, "Eliminar miembro")
    db.commit()
