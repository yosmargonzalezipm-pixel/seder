from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Familia, Miembro, Parentesco
from app.schemas.familia import FamiliaCreate, FamiliaUpdate, FamiliaOut, AsignarMiembroBody
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
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
    familias = query.order_by(Familia.Nombre_Familia).all()
    return [
        FamiliaOut(
            ID_Familia=f.ID_Familia,
            Nombre_Familia=f.Nombre_Familia,
            ID_Cabeza_Familia=f.ID_Cabeza_Familia,
            Cabeza_Familia_Nombre=f"{f.cabeza_familia.Nombres} {f.cabeza_familia.Apellidos}" if f.cabeza_familia else None,
            Num_Miembros=db.query(Miembro).filter(Miembro.ID_Familia == f.ID_Familia).count(),
        )
        for f in familias
    ]


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
    return FamiliaOut(
        ID_Familia=familia.ID_Familia,
        Nombre_Familia=familia.Nombre_Familia,
        ID_Cabeza_Familia=familia.ID_Cabeza_Familia,
        Cabeza_Familia_Nombre=f"{familia.cabeza_familia.Nombres} {familia.cabeza_familia.Apellidos}" if familia.cabeza_familia else None,
        Num_Miembros=db.query(Miembro).filter(Miembro.ID_Familia == familia_id).count(),
    )


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
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Familias", familia.ID_Familia, "Crear familia")
    db.commit()
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
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Familias", familia.ID_Familia, "Actualizar familia")
    db.commit()
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
    id_familia = familia.ID_Familia
    db.delete(familia)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Familias", id_familia, "Eliminar familia")
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
        {
            "ID_Miembro": m.ID_Miembro,
            "Cedula": m.Cedula,
            "Nombres": m.Nombres,
            "Apellidos": m.Apellidos,
            "ID_Parentesco": m.ID_Parentesco,
            "Parentesco": m.parentesco_rel.Nombre if m.parentesco_rel else None,
        }
        for m in miembros
    ]


@router.post("/{familia_id}/miembros/{miembro_id}", status_code=200)
def asignar_miembro_a_familia(
    familia_id: int,
    miembro_id: int,
    body: AsignarMiembroBody,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    familia = db.query(Familia).filter(Familia.ID_Familia == familia_id).first()
    if not familia:
        raise HTTPException(status_code=404, detail="Familia no encontrada")
    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    miembro.ID_Familia = familia_id
    miembro.ID_Parentesco = body.ID_Parentesco
    db.commit()
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Familias", familia_id, f"Asignar miembro {miembro_id} a familia")
    db.commit()
    return {"mensaje": "Miembro asignado a la familia"}


@router.delete("/{familia_id}/miembros/{miembro_id}", status_code=200)
def quitar_miembro_de_familia(
    familia_id: int,
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "familias.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id, Miembro.ID_Familia == familia_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado en esta familia")
    miembro.ID_Familia = None
    miembro.ID_Parentesco = None
    db.commit()
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Familias", familia_id, f"Quitar miembro {miembro_id} de familia")
    db.commit()
    return {"mensaje": "Miembro quitado de la familia"}
