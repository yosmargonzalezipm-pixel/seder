from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario, Permiso, RolPermiso
from app.models.miembro import Miembro
from app.schemas.auth import LoginRequest, LoginResponse, UsuarioInfo, PermisoInfo
from app.utils.security import (
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        (Usuario.Nombre_Usuario == data.usuario) | (Usuario.Email == data.usuario)
    ).first()

    if not usuario or not verify_password(data.password, usuario.Password_Hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if not usuario.Activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador.",
        )

    usuario.Ultimo_Acceso = datetime.now(timezone.utc)
    db.commit()

    token = create_access_token({"sub": str(usuario.ID_Usuario), "rol": usuario.rol.Nombre_Rol})

    nombre_completo = None
    if usuario.ID_Miembro and usuario.miembro:
        nombre_completo = f"{usuario.miembro.Nombres} {usuario.miembro.Apellidos}"

    return LoginResponse(
        access_token=token,
        usuario=usuario.Nombre_Usuario,
        rol=usuario.rol.Nombre_Rol,
        nombre_completo=nombre_completo,
    )


@router.get("/me", response_model=UsuarioInfo)
def me(usuario: Usuario = Depends(get_current_user)):
    return UsuarioInfo(
        ID_Usuario=usuario.ID_Usuario,
        Nombre_Usuario=usuario.Nombre_Usuario,
        Email=usuario.Email,
        Rol=usuario.rol.Nombre_Rol,
        Activo=usuario.Activo,
    )


@router.get("/permisos", response_model=list[PermisoInfo])
def mis_permisos(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if usuario.rol.Nombre_Rol == "Administrador":
        permisos = db.query(Permiso).all()
    else:
        permisos = (
            db.query(Permiso)
            .join(RolPermiso)
            .filter(RolPermiso.ID_Rol == usuario.ID_Rol)
            .all()
        )

    return [PermisoInfo(Nombre_Permiso=p.Nombre_Permiso) for p in permisos]
