from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.auditoria import Auditoria
from app.schemas.auditoria import AuditoriaOut
from app.utils.security import get_current_user, tiene_permiso
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/auditoria", tags=["Auditoría"])


@router.get("", response_model=list[AuditoriaOut])
def listar_auditoria(
    q: str = Query(""),
    accion: str = Query(None),
    tabla: str = Query(None),
    desde: str = Query(None),
    hasta: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "auditoria.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    query = db.query(Auditoria)

    if accion:
        query = query.filter(Auditoria.Accion == accion)
    if tabla:
        query = query.filter(Auditoria.Tabla_Afectada == tabla)
    if desde:
        query = query.filter(Auditoria.Fecha_Hora >= desde)
    if hasta:
        query = query.filter(Auditoria.Fecha_Hora <= hasta)
    if q:
        query = query.filter(
            or_(
                Auditoria.Detalle.ilike(f"%{q}%"),
                Auditoria.Accion.ilike(f"%{q}%"),
            )
        )

    registros = query.order_by(Auditoria.Fecha_Hora.desc()).offset(skip).limit(limit).all()

    return [
        AuditoriaOut(
            ID_Auditoria=a.ID_Auditoria,
            ID_Usuario=a.ID_Usuario,
            Usuario_Nombre=a.usuario.Nombre_Usuario if a.usuario else "Sistema",
            Accion=a.Accion,
            Tabla_Afectada=a.Tabla_Afectada,
            ID_Registro_Afectado=a.ID_Registro_Afectado,
            Detalle=a.Detalle,
            Direccion_IP=a.Direccion_IP,
            Fecha_Hora=a.Fecha_Hora,
        )
        for a in registros
    ]


@router.get("/acciones")
def listar_acciones(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "auditoria.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    from sqlalchemy import func
    acciones = db.query(Auditoria.Accion, func.count(Auditoria.ID_Auditoria)).group_by(Auditoria.Accion).order_by(Auditoria.Accion).all()
    return [{"accion": a, "total": c} for a, c in acciones]


@router.get("/{auditoria_id}", response_model=AuditoriaOut)
def obtener_auditoria(
    auditoria_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "auditoria.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    a = db.query(Auditoria).filter(Auditoria.ID_Auditoria == auditoria_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return AuditoriaOut(
        ID_Auditoria=a.ID_Auditoria,
        ID_Usuario=a.ID_Usuario,
        Usuario_Nombre=a.usuario.Nombre_Usuario if a.usuario else "Sistema",
        Accion=a.Accion,
        Tabla_Afectada=a.Tabla_Afectada,
        ID_Registro_Afectado=a.ID_Registro_Afectado,
        Detalle=a.Detalle,
        Direccion_IP=a.Direccion_IP,
        Fecha_Hora=a.Fecha_Hora,
    )
