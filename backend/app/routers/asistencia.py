from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.asistencia import RegistroAsistencia
from app.models import Miembro
from app.schemas.asistencia import AsistenciaCreate, AsistenciaUpdate, AsistenciaOut
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/asistencia", tags=["Asistencia"])


@router.get("", response_model=list[AsistenciaOut])
def listar_asistencia(
    q: str = Query(""),
    fecha_desde: str = Query(None),
    fecha_hasta: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "asistencia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    query = db.query(RegistroAsistencia)

    if q:
        query = query.join(Miembro).filter(
            or_(
                Miembro.Nombres.ilike(f"%{q}%"),
                Miembro.Apellidos.ilike(f"%{q}%"),
            )
        )
    if fecha_desde:
        query = query.filter(RegistroAsistencia.Fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(RegistroAsistencia.Fecha <= fecha_hasta)

    registros = query.order_by(RegistroAsistencia.Fecha.desc()).offset(skip).limit(limit).all()

    return [
        AsistenciaOut(
            ID_Asistencia=r.ID_Asistencia,
            ID_Miembro=r.ID_Miembro,
            Fecha=r.Fecha,
            Tipo_Evento=r.Tipo_Evento,
            Estado_Asistencia=r.Estado_Asistencia,
            Miembro_Nombre=f"{r.miembro.Nombres} {r.miembro.Apellidos}" if r.miembro else "",
        )
        for r in registros
    ]


@router.get("/{asistencia_id}", response_model=AsistenciaOut)
def obtener_asistencia(
    asistencia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "asistencia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(RegistroAsistencia).filter(RegistroAsistencia.ID_Asistencia == asistencia_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return AsistenciaOut(
        ID_Asistencia=r.ID_Asistencia,
        ID_Miembro=r.ID_Miembro,
        Fecha=r.Fecha,
        Tipo_Evento=r.Tipo_Evento,
        Estado_Asistencia=r.Estado_Asistencia,
        Miembro_Nombre=f"{r.miembro.Nombres} {r.miembro.Apellidos}" if r.miembro else "",
    )


@router.post("", response_model=AsistenciaOut, status_code=201)
def crear_asistencia(
    data: AsistenciaCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "asistencia.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == data.ID_Miembro).first()
    if not miembro:
        raise HTTPException(status_code=400, detail="Miembro no encontrado")

    r = RegistroAsistencia(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Asistencia", r.ID_Asistencia, "Crear asistencia")
    db.commit()

    return AsistenciaOut(
        ID_Asistencia=r.ID_Asistencia,
        ID_Miembro=r.ID_Miembro,
        Fecha=r.Fecha,
        Tipo_Evento=r.Tipo_Evento,
        Estado_Asistencia=r.Estado_Asistencia,
        Miembro_Nombre=f"{miembro.Nombres} {miembro.Apellidos}",
    )


@router.put("/{asistencia_id}", response_model=AsistenciaOut)
def actualizar_asistencia(
    asistencia_id: int,
    data: AsistenciaUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "asistencia.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(RegistroAsistencia).filter(RegistroAsistencia.ID_Asistencia == asistencia_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(r, key, val)
    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Asistencia", r.ID_Asistencia, "Actualizar asistencia")
    db.commit()

    return AsistenciaOut(
        ID_Asistencia=r.ID_Asistencia,
        ID_Miembro=r.ID_Miembro,
        Fecha=r.Fecha,
        Tipo_Evento=r.Tipo_Evento,
        Estado_Asistencia=r.Estado_Asistencia,
        Miembro_Nombre=f"{r.miembro.Nombres} {r.miembro.Apellidos}" if r.miembro else "",
    )


@router.delete("/{asistencia_id}", status_code=204)
def eliminar_asistencia(
    asistencia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "asistencia.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(RegistroAsistencia).filter(RegistroAsistencia.ID_Asistencia == asistencia_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    id_asistencia = r.ID_Asistencia
    db.delete(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Asistencia", id_asistencia, "Eliminar asistencia")
    db.commit()
