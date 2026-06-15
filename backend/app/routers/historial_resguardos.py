from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.inventario import HistorialResguardo, Inventario
from app.models import Miembro
from app.schemas.historial_resguardo import (
    HistorialResguardoCreate,
    HistorialResguardoUpdate,
    HistorialResguardoOut,
    HistorialResguardoListOut,
)
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/resguardos", tags=["Historial Resguardos"])


@router.get("", response_model=list[HistorialResguardoListOut])
def listar_resguardos(
    q: str = Query(""),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "historial_resguardo.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    query = db.query(HistorialResguardo)
    if q:
        query = (
            query.outerjoin(Inventario)
            .outerjoin(Miembro)
            .filter(
                or_(
                    Inventario.Nombre_Articulo.ilike(f"%{q}%"),
                    Miembro.Nombres.ilike(f"%{q}%"),
                    Miembro.Apellidos.ilike(f"%{q}%"),
                )
            )
        )

    resguardos = query.order_by(HistorialResguardo.Fecha_Salida_Asignacion.desc()).offset(skip).limit(limit).all()

    return [
        HistorialResguardoListOut(
            ID_Resguardo=r.ID_Resguardo,
            ID_Articulo=r.ID_Articulo,
            Nombre_Articulo=r.articulo.Nombre_Articulo if r.articulo else "",
            ID_Miembro_Responsable=r.ID_Miembro_Responsable,
            Nombre_Miembro=f"{r.miembro_responsable.Nombres} {r.miembro_responsable.Apellidos}" if r.miembro_responsable else "",
            Fecha_Salida_Asignacion=r.Fecha_Salida_Asignacion,
            Fecha_Devolucion_Prevista=r.Fecha_Devolucion_Prevista,
            Estado_Entrega=r.Estado_Entrega,
            Estado_Devolucion=r.Estado_Devolucion,
        )
        for r in resguardos
    ]


@router.get("/articulo/{articulo_id}", response_model=list[HistorialResguardoListOut])
def listar_resguardos_por_articulo(
    articulo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "historial_resguardo.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    resguardos = (
        db.query(HistorialResguardo)
        .filter(HistorialResguardo.ID_Articulo == articulo_id)
        .order_by(HistorialResguardo.Fecha_Salida_Asignacion.desc())
        .all()
    )

    return [
        HistorialResguardoListOut(
            ID_Resguardo=r.ID_Resguardo,
            ID_Articulo=r.ID_Articulo,
            Nombre_Articulo=r.articulo.Nombre_Articulo if r.articulo else "",
            ID_Miembro_Responsable=r.ID_Miembro_Responsable,
            Nombre_Miembro=f"{r.miembro_responsable.Nombres} {r.miembro_responsable.Apellidos}" if r.miembro_responsable else "",
            Fecha_Salida_Asignacion=r.Fecha_Salida_Asignacion,
            Fecha_Devolucion_Prevista=r.Fecha_Devolucion_Prevista,
            Estado_Entrega=r.Estado_Entrega,
            Estado_Devolucion=r.Estado_Devolucion,
        )
        for r in resguardos
    ]


@router.get("/{resguardo_id}", response_model=HistorialResguardoOut)
def obtener_resguardo(
    resguardo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "historial_resguardo.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(HistorialResguardo).filter(HistorialResguardo.ID_Resguardo == resguardo_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resguardo no encontrado")
    return r


@router.post("", response_model=HistorialResguardoOut, status_code=201)
def crear_resguardo(
    data: HistorialResguardoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "historial_resguardo.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = HistorialResguardo(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Historial Resguardos", r.ID_Resguardo, "Crear resguardo")
    db.commit()
    return r


@router.put("/{resguardo_id}", response_model=HistorialResguardoOut)
def actualizar_resguardo(
    resguardo_id: int,
    data: HistorialResguardoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "historial_resguardo.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(HistorialResguardo).filter(HistorialResguardo.ID_Resguardo == resguardo_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resguardo no encontrado")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(r, key, val)
    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Historial Resguardos", r.ID_Resguardo, "Actualizar resguardo")
    db.commit()
    return r


@router.delete("/{resguardo_id}", status_code=204)
def eliminar_resguardo(
    resguardo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "historial_resguardo.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(HistorialResguardo).filter(HistorialResguardo.ID_Resguardo == resguardo_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Resguardo no encontrado")

    id_r = r.ID_Resguardo
    db.delete(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Historial Resguardos", id_r, "Eliminar resguardo")
    db.commit()
