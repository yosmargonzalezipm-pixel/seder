from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Usuario, Rol, Miembro
from app.schemas.usuario_gestion import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.utils.security import get_current_user, tiene_permiso, hash_password
from app.models.usuario import Usuario as UsuarioModel

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios(
    q: str = Query(""),
    usuario: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "usuarios.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    query = db.query(Usuario)
    if q:
        query = query.filter(
            or_(
                Usuario.Nombre_Usuario.ilike(f"%{q}%"),
                Usuario.Email.ilike(f"%{q}%"),
            )
        )
    usuarios = query.order_by(Usuario.Nombre_Usuario).all()

    return [
        UsuarioOut(
            ID_Usuario=u.ID_Usuario,
            Nombre_Usuario=u.Nombre_Usuario,
            Email=u.Email,
            ID_Rol=u.ID_Rol,
            Rol_Nombre=u.rol.Nombre_Rol if u.rol else "",
            Activo=u.Activo,
            Ultimo_Acceso=u.Ultimo_Acceso.isoformat() if u.Ultimo_Acceso else None,
            Miembro_Nombre=f"{u.miembro.Nombres} {u.miembro.Apellidos}" if u.miembro else "",
        )
        for u in usuarios
    ]


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(
    usuario_id: int,
    usuario: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "usuarios.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    u = db.query(Usuario).filter(Usuario.ID_Usuario == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UsuarioOut(
        ID_Usuario=u.ID_Usuario,
        Nombre_Usuario=u.Nombre_Usuario,
        Email=u.Email,
        ID_Rol=u.ID_Rol,
        Rol_Nombre=u.rol.Nombre_Rol if u.rol else "",
        Activo=u.Activo,
        Ultimo_Acceso=u.Ultimo_Acceso.isoformat() if u.Ultimo_Acceso else None,
        Miembro_Nombre=f"{u.miembro.Nombres} {u.miembro.Apellidos}" if u.miembro else "",
    )


@router.post("", response_model=UsuarioOut, status_code=201)
def crear_usuario(
    data: UsuarioCreate,
    usuario: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "usuarios.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    existe = db.query(Usuario).filter(
        (Usuario.Nombre_Usuario == data.Nombre_Usuario) | (Usuario.Email == data.Email)
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese nombre o email")

    if not db.query(Rol).filter(Rol.ID_Rol == data.ID_Rol).first():
        raise HTTPException(status_code=400, detail="Rol no encontrado")

    u = Usuario(
        Nombre_Usuario=data.Nombre_Usuario,
        Email=data.Email,
        Password_Hash=hash_password(data.Password),
        ID_Rol=data.ID_Rol,
        ID_Miembro=data.ID_Miembro,
        Activo=data.Activo,
    )
    db.add(u)
    db.commit()
    db.refresh(u)

    return UsuarioOut(
        ID_Usuario=u.ID_Usuario,
        Nombre_Usuario=u.Nombre_Usuario,
        Email=u.Email,
        ID_Rol=u.ID_Rol,
        Rol_Nombre=u.rol.Nombre_Rol if u.rol else "",
        Activo=u.Activo,
        Ultimo_Acceso=None,
        Miembro_Nombre=f"{u.miembro.Nombres} {u.miembro.Apellidos}" if u.miembro else "",
    )


@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    usuario: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "usuarios.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    u = db.query(Usuario).filter(Usuario.ID_Usuario == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    updates = data.model_dump(exclude_unset=True)
    if "Password" in updates:
        updates["Password_Hash"] = hash_password(updates.pop("Password"))
    if "Nombre_Usuario" in updates:
        del updates["Nombre_Usuario"]
    if "Email" in updates and updates["Email"] != u.Email:
        existe = db.query(Usuario).filter(Usuario.Email == updates["Email"]).first()
        if existe:
            raise HTTPException(status_code=400, detail="Email ya en uso")

    for key, val in updates.items():
        setattr(u, key, val)
    db.commit()
    db.refresh(u)

    return UsuarioOut(
        ID_Usuario=u.ID_Usuario,
        Nombre_Usuario=u.Nombre_Usuario,
        Email=u.Email,
        ID_Rol=u.ID_Rol,
        Rol_Nombre=u.rol.Nombre_Rol if u.rol else "",
        Activo=u.Activo,
        Ultimo_Acceso=u.Ultimo_Acceso.isoformat() if u.Ultimo_Acceso else None,
        Miembro_Nombre=f"{u.miembro.Nombres} {u.miembro.Apellidos}" if u.miembro else "",
    )


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(
    usuario_id: int,
    usuario: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "usuarios.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    if usuario_id == usuario.ID_Usuario:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")

    u = db.query(Usuario).filter(Usuario.ID_Usuario == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(u)
    db.commit()


@router.put("/{usuario_id}/toggle-activo")
def toggle_activo(
    usuario_id: int,
    usuario: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "usuarios.gestionar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    if usuario_id == usuario.ID_Usuario:
        raise HTTPException(status_code=400, detail="No puedes desactivarte a ti mismo")

    u = db.query(Usuario).filter(Usuario.ID_Usuario == usuario_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    u.Activo = not u.Activo
    db.commit()
    return {"Activo": u.Activo}
