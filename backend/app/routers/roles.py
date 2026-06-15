from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Rol, Permiso, RolPermiso, Usuario
from app.schemas.rol import RolCreate, RolUpdate, RolOut, PermisoOut
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria

router = APIRouter(prefix="/api/roles", tags=["Roles"])


@router.get("", response_model=list[RolOut])
def listar_roles(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    roles = db.query(Rol).order_by(Rol.Nombre_Rol).all()
    result = []
    for r in roles:
        permiso_ids = [rp.ID_Permiso for rp in r.permisos]
        result.append(RolOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion, permisos=permiso_ids))
    return result


@router.get("/permisos", response_model=list[PermisoOut])
def listar_permisos(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    return db.query(Permiso).order_by(Permiso.Nombre_Permiso).all()


@router.get("/{rol_id}", response_model=RolOut)
def obtener_rol(
    rol_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(Rol).filter(Rol.ID_Rol == rol_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    permiso_ids = [rp.ID_Permiso for rp in r.permisos]
    return RolOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion, permisos=permiso_ids)


@router.post("", response_model=RolOut, status_code=201)
def crear_rol(
    data: RolCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    existe = db.query(Rol).filter(Rol.Nombre_Rol == data.Nombre_Rol).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")

    r = Rol(Nombre_Rol=data.Nombre_Rol, Descripcion=data.Descripcion)
    db.add(r)
    db.flush()

    for pid in data.permisos:
        if db.query(Permiso).filter(Permiso.ID_Permiso == pid).first():
            db.add(RolPermiso(ID_Rol=r.ID_Rol, ID_Permiso=pid))

    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Roles", r.ID_Rol, "Crear rol")
    db.commit()
    permiso_ids = [rp.ID_Permiso for rp in r.permisos]
    return RolOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion, permisos=permiso_ids)


@router.put("/{rol_id}", response_model=RolOut)
def actualizar_rol(
    rol_id: int,
    data: RolUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    r = db.query(Rol).filter(Rol.ID_Rol == rol_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if data.Nombre_Rol is not None:
        r.Nombre_Rol = data.Nombre_Rol
    if data.Descripcion is not None:
        r.Descripcion = data.Descripcion

    if data.permisos is not None:
        db.query(RolPermiso).filter(RolPermiso.ID_Rol == rol_id).delete()
        for pid in data.permisos:
            if db.query(Permiso).filter(Permiso.ID_Permiso == pid).first():
                db.add(RolPermiso(ID_Rol=rol_id, ID_Permiso=pid))

    db.commit()
    db.refresh(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Roles", r.ID_Rol, "Actualizar rol")
    db.commit()
    permiso_ids = [rp.ID_Permiso for rp in r.permisos]
    return RolOut(ID_Rol=r.ID_Rol, Nombre_Rol=r.Nombre_Rol, Descripcion=r.Descripcion, permisos=permiso_ids)


@router.delete("/{rol_id}", status_code=204)
def eliminar_rol(
    rol_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "roles.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    if rol_id == 1:
        raise HTTPException(status_code=400, detail="No se puede eliminar el rol Administrador")

    usuarios = db.query(Usuario).filter(Usuario.ID_Rol == rol_id).count()
    if usuarios > 0:
        raise HTTPException(status_code=400, detail=f"No se puede eliminar: {usuarios} usuario(s) tienen este rol")

    r = db.query(Rol).filter(Rol.ID_Rol == rol_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    db.query(RolPermiso).filter(RolPermiso.ID_Rol == rol_id).delete()
    id_rol = r.ID_Rol
    db.delete(r)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Roles", id_rol, "Eliminar rol")
    db.commit()
