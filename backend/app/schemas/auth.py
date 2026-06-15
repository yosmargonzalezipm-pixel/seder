from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    usuario: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: str
    rol: str
    nombre_completo: str | None = None


class UsuarioInfo(BaseModel):
    ID_Usuario: int
    Nombre_Usuario: str
    Email: str
    Rol: str
    Activo: bool

    class Config:
        from_attributes = True


class PermisoInfo(BaseModel):
    Nombre_Permiso: str

    class Config:
        from_attributes = True
