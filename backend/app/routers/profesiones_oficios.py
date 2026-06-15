from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profesion, Oficio
from app.schemas.profesion_oficio import CatalogoCreate, CatalogoUpdate, CatalogoOut
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/catalogos", tags=["Catálogos"])


@router.get("/profesiones", response_model=list[CatalogoOut])
def listar_profesiones(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "profesiones.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Profesion)
    if q:
        query = query.filter(Profesion.Nombre_Profesion.ilike(f"%{q}%"))
    return [CatalogoOut(ID=p.ID_Profesion, Nombre=p.Nombre_Profesion) for p in query.order_by(Profesion.Nombre_Profesion).all()]


@router.get("/profesiones/{profesion_id}", response_model=CatalogoOut)
def obtener_profesion(
    profesion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "profesiones.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Profesion).filter(Profesion.ID_Profesion == profesion_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profesión no encontrada")
    return CatalogoOut(ID=p.ID_Profesion, Nombre=p.Nombre_Profesion)


@router.post("/profesiones", response_model=CatalogoOut, status_code=201)
def crear_profesion(
    data: CatalogoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "profesiones.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = Profesion(Nombre_Profesion=data.Nombre)
    db.add(p)
    db.commit()
    db.refresh(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Profesiones", p.ID_Profesion, "Crear profesión")
    db.commit()
    return CatalogoOut(ID=p.ID_Profesion, Nombre=p.Nombre_Profesion)


@router.put("/profesiones/{profesion_id}", response_model=CatalogoOut)
def actualizar_profesion(
    profesion_id: int,
    data: CatalogoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "profesiones.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Profesion).filter(Profesion.ID_Profesion == profesion_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profesión no encontrada")
    if data.Nombre is not None:
        p.Nombre_Profesion = data.Nombre
    db.commit()
    db.refresh(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Profesiones", p.ID_Profesion, "Actualizar profesión")
    db.commit()
    return CatalogoOut(ID=p.ID_Profesion, Nombre=p.Nombre_Profesion)


@router.delete("/profesiones/{profesion_id}", status_code=204)
def eliminar_profesion(
    profesion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "profesiones.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Profesion).filter(Profesion.ID_Profesion == profesion_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Profesión no encontrada")
    id_p = p.ID_Profesion
    db.delete(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Profesiones", id_p, "Eliminar profesión")
    db.commit()


@router.get("/oficios", response_model=list[CatalogoOut])
def listar_oficios(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "oficios.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Oficio)
    if q:
        query = query.filter(Oficio.Nombre_Oficio.ilike(f"%{q}%"))
    return [CatalogoOut(ID=o.ID_Oficio, Nombre=o.Nombre_Oficio) for o in query.order_by(Oficio.Nombre_Oficio).all()]


@router.get("/oficios/{oficio_id}", response_model=CatalogoOut)
def obtener_oficio(
    oficio_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "oficios.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    o = db.query(Oficio).filter(Oficio.ID_Oficio == oficio_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Oficio no encontrado")
    return CatalogoOut(ID=o.ID_Oficio, Nombre=o.Nombre_Oficio)


@router.post("/oficios", response_model=CatalogoOut, status_code=201)
def crear_oficio(
    data: CatalogoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "oficios.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    o = Oficio(Nombre_Oficio=data.Nombre)
    db.add(o)
    db.commit()
    db.refresh(o)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Oficios", o.ID_Oficio, "Crear oficio")
    db.commit()
    return CatalogoOut(ID=o.ID_Oficio, Nombre=o.Nombre_Oficio)


@router.put("/oficios/{oficio_id}", response_model=CatalogoOut)
def actualizar_oficio(
    oficio_id: int,
    data: CatalogoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "oficios.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    o = db.query(Oficio).filter(Oficio.ID_Oficio == oficio_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Oficio no encontrado")
    if data.Nombre is not None:
        o.Nombre_Oficio = data.Nombre
    db.commit()
    db.refresh(o)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Oficios", o.ID_Oficio, "Actualizar oficio")
    db.commit()
    return CatalogoOut(ID=o.ID_Oficio, Nombre=o.Nombre_Oficio)


@router.delete("/oficios/{oficio_id}", status_code=204)
def eliminar_oficio(
    oficio_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "oficios.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    o = db.query(Oficio).filter(Oficio.ID_Oficio == oficio_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Oficio no encontrado")
    id_o = o.ID_Oficio
    db.delete(o)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Oficios", id_o, "Eliminar oficio")
    db.commit()
