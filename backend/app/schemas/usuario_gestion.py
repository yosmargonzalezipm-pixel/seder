from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    Nombre_Usuario: str
    Email: EmailStr
    Password: str
    ID_Rol: int
    ID_Miembro: int | None = None
    Activo: bool = True


class UsuarioUpdate(BaseModel):
    Email: EmailStr | None = None
    Password: str | None = None
    ID_Rol: int | None = None
    ID_Miembro: int | None = None
    Activo: bool | None = None


class UsuarioOut(BaseModel):
    ID_Usuario: int
    Nombre_Usuario: str
    Email: str
    ID_Rol: int
    Rol_Nombre: str = ""
    Activo: bool
    Ultimo_Acceso: str | None = None
    Miembro_Nombre: str = ""

    class Config:
        from_attributes = True
