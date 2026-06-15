from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Iglesia, Ciudad, Parroquia
from app.schemas.iglesia import IglesiaCreate, IglesiaUpdate, IglesiaOut
from app.utils.security import get_current_user, tiene_permiso
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/iglesias", tags=["Iglesias"])


@router.get("", response_model=list[IglesiaOut])
def listar_iglesias(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "iglesias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Iglesia)
    if q:
        query = query.filter(Iglesia.Nombre_Iglesia.ilike(f"%{q}%"))
    iglesias = query.order_by(Iglesia.Nombre_Iglesia).all()
    return [
        IglesiaOut(
            ID_Iglesia=i.ID_Iglesia,
            Nombre_Iglesia=i.Nombre_Iglesia,
            ID_Iglesia_Madre=i.ID_Iglesia_Madre,
            Direccion=i.Direccion,
            Telefono_Iglesia_movil=i.Telefono_Iglesia_movil,
            Telefono_fijo=i.Telefono_fijo,
            Correo=i.Correo,
            ID_Ciudad=i.ID_Ciudad,
            ID_Parroquia=i.ID_Parroquia,
            Iglesia_Madre_Nombre=i.iglesia_madre.Nombre_Iglesia if i.iglesia_madre else "",
            Ciudad_Nombre=i.ciudad.Nombre_Ciudad if i.ciudad else "",
            Parroquia_Nombre=i.parroquia.Nombre_Parroquia if i.parroquia else "",
            Creado_En=i.Creado_En,
            Actualizado_En=i.Actualizado_En,
        )
        for i in iglesias
    ]


@router.get("/{iglesia_id}", response_model=IglesiaOut)
def obtener_iglesia(
    iglesia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "iglesias.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    i = db.query(Iglesia).filter(Iglesia.ID_Iglesia == iglesia_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Iglesia no encontrada")
    return IglesiaOut(
        ID_Iglesia=i.ID_Iglesia,
        Nombre_Iglesia=i.Nombre_Iglesia,
        ID_Iglesia_Madre=i.ID_Iglesia_Madre,
        Direccion=i.Direccion,
        Telefono_Iglesia_movil=i.Telefono_Iglesia_movil,
        Telefono_fijo=i.Telefono_fijo,
        Correo=i.Correo,
        ID_Ciudad=i.ID_Ciudad,
        ID_Parroquia=i.ID_Parroquia,
        Iglesia_Madre_Nombre=i.iglesia_madre.Nombre_Iglesia if i.iglesia_madre else "",
        Ciudad_Nombre=i.ciudad.Nombre_Ciudad if i.ciudad else "",
        Parroquia_Nombre=i.parroquia.Nombre_Parroquia if i.parroquia else "",
        Creado_En=i.Creado_En,
        Actualizado_En=i.Actualizado_En,
    )


@router.post("", response_model=IglesiaOut, status_code=201)
def crear_iglesia(
    data: IglesiaCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "iglesias.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    i = Iglesia(**data.model_dump())
    db.add(i)
    db.commit()
    db.refresh(i)
    return IglesiaOut(
        ID_Iglesia=i.ID_Iglesia,
        Nombre_Iglesia=i.Nombre_Iglesia,
        ID_Iglesia_Madre=i.ID_Iglesia_Madre,
        Direccion=i.Direccion,
        Telefono_Iglesia_movil=i.Telefono_Iglesia_movil,
        Telefono_fijo=i.Telefono_fijo,
        Correo=i.Correo,
        ID_Ciudad=i.ID_Ciudad,
        ID_Parroquia=i.ID_Parroquia,
        Iglesia_Madre_Nombre=i.iglesia_madre.Nombre_Iglesia if i.iglesia_madre else "",
        Ciudad_Nombre=i.ciudad.Nombre_Ciudad if i.ciudad else "",
        Parroquia_Nombre=i.parroquia.Nombre_Parroquia if i.parroquia else "",
        Creado_En=i.Creado_En,
        Actualizado_En=i.Actualizado_En,
    )


@router.put("/{iglesia_id}", response_model=IglesiaOut)
def actualizar_iglesia(
    iglesia_id: int,
    data: IglesiaUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "iglesias.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    i = db.query(Iglesia).filter(Iglesia.ID_Iglesia == iglesia_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Iglesia no encontrada")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(i, key, val)
    db.commit()
    db.refresh(i)
    return IglesiaOut(
        ID_Iglesia=i.ID_Iglesia,
        Nombre_Iglesia=i.Nombre_Iglesia,
        ID_Iglesia_Madre=i.ID_Iglesia_Madre,
        Direccion=i.Direccion,
        Telefono_Iglesia_movil=i.Telefono_Iglesia_movil,
        Telefono_fijo=i.Telefono_fijo,
        Correo=i.Correo,
        ID_Ciudad=i.ID_Ciudad,
        ID_Parroquia=i.ID_Parroquia,
        Iglesia_Madre_Nombre=i.iglesia_madre.Nombre_Iglesia if i.iglesia_madre else "",
        Ciudad_Nombre=i.ciudad.Nombre_Ciudad if i.ciudad else "",
        Parroquia_Nombre=i.parroquia.Nombre_Parroquia if i.parroquia else "",
        Creado_En=i.Creado_En,
        Actualizado_En=i.Actualizado_En,
    )


@router.delete("/{iglesia_id}", status_code=204)
def eliminar_iglesia(
    iglesia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "iglesias.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    i = db.query(Iglesia).filter(Iglesia.ID_Iglesia == iglesia_id).first()
    if not i:
        raise HTTPException(status_code=404, detail="Iglesia no encontrada")
    db.delete(i)
    db.commit()
