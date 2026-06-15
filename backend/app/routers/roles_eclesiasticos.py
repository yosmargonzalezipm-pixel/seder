from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.miembro import Miembro, MiembroRol
from app.models.usuario import Rol, Usuario
from app.schemas.rol_eclesiastico import (
    RolEclesiasticoCreate, RolEclesiasticoUpdate, RolEclesiasticoOut,
    MiembroRolAsignar, MiembroRolOut,
)
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria

router = APIRouter(prefix="/api/roles-eclesiasticos", tags=["Roles Eclesiásticos"])

# --- CRUD de roles eclesiásticos (en tabla Roles compartida) ---


@router.get("", response_model=list[RolEclesiasticoOut])
def listar_roles_eclesiasticos(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    roles = db.query(Rol).order_by(Rol.Nombre_Rol).all()
    result = []
    for r in roles:
        total = db.query(MiembroRol).filter(MiembroRol.ID_Rol == r.ID_Rol).count()
        result.append(RolEclesiasticoOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion, Total_Miembros=total))
    return result


@router.post("", response_model=RolEclesiasticoOut, status_code=201)
def crear_rol_eclesiastico(
    data: RolEclesiasticoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    existe = db.query(Rol).filter(Rol.Nombre_Rol == data.Nombre_Rol).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")
    r = Rol(Nombre_Rol=data.Nombre_Rol, Descripcion=data.Descripcion)
    db.add(r)
    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Roles Eclesiásticos", r.ID_Rol, "Crear rol eclesiástico")
    db.commit()
    return RolEclesiasticoOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion)


@router.put("/{rol_id}", response_model=RolEclesiasticoOut)
def actualizar_rol_eclesiastico(
    rol_id: int,
    data: RolEclesiasticoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    r = db.query(Rol).filter(Rol.ID_Rol == rol_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if data.Nombre_Rol is not None:
        r.Nombre_Rol = data.Nombre_Rol
    if data.Descripcion is not None:
        r.Descripcion = data.Descripcion
    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Roles Eclesiásticos", r.ID_Rol, "Actualizar rol eclesiástico")
    db.commit()
    total = db.query(MiembroRol).filter(MiembroRol.ID_Rol == rol_id).count()
    return RolEclesiasticoOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion, Total_Miembros=total)


@router.delete("/{rol_id}", status_code=204)
def eliminar_rol_eclesiastico(
    rol_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    if rol_id <= 3:
        raise HTTPException(status_code=400, detail="No se puede eliminar roles del sistema")
    r = db.query(Rol).filter(Rol.ID_Rol == rol_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.query(MiembroRol).filter(MiembroRol.ID_Rol == rol_id).delete()
    id_rol = r.ID_Rol
    db.delete(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Roles Eclesiásticos", id_rol, "Eliminar rol eclesiástico")
    db.commit()

# --- Asignación de roles a miembros ---


@router.get("/miembro/{miembro_id}", response_model=list[MiembroRolOut])
def listar_roles_de_miembro(
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    asignaciones = db.query(MiembroRol).filter(MiembroRol.ID_Miembro == miembro_id).all()
    return [
        MiembroRolOut(
            ID_Rol=a.ID_Rol,
            Nombre_Rol=a.rol.Nombre_Rol if a.rol else "",
            Fecha_Asignacion=a.Fecha_Asignacion,
            Estado_Rol=a.Estado_Rol,
        )
        for a in asignaciones
    ]


@router.post("/miembro/{miembro_id}")
def asignar_rol(
    miembro_id: int,
    data: MiembroRolAsignar,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    rol = db.query(Rol).filter(Rol.ID_Rol == data.ID_Rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    existe = db.query(MiembroRol).filter(MiembroRol.ID_Miembro == miembro_id, MiembroRol.ID_Rol == data.ID_Rol).first()
    if existe:
        raise HTTPException(status_code=400, detail="El miembro ya tiene este rol asignado")
    mr = MiembroRol(ID_Miembro=miembro_id, ID_Rol=data.ID_Rol, Fecha_Asignacion=data.Fecha_Asignacion, Estado_Rol=data.Estado_Rol)
    db.add(mr)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Roles Eclesiásticos", None, f"Asignar rol eclesiástico a miembro {miembro_id}")
    db.commit()
    return {"mensaje": "Rol asignado correctamente"}


@router.delete("/miembro/{miembro_id}/rol/{rol_id}", status_code=204)
def remover_rol(
    miembro_id: int,
    rol_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles_eclesiasticos.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    mr = db.query(MiembroRol).filter(MiembroRol.ID_Miembro == miembro_id, MiembroRol.ID_Rol == rol_id).first()
    if not mr:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    db.delete(mr)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Roles Eclesiásticos", None, f"Remover rol eclesiástico de miembro {miembro_id}")
    db.commit()
