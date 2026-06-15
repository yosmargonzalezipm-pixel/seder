from pydantic import BaseModel


class RolCreate(BaseModel):
    Nombre_Rol: str
    Descripcion: str | None = None
    permisos: list[int] = []


class RolUpdate(BaseModel):
    Nombre_Rol: str | None = None
    Descripcion: str | None = None
    permisos: list[int] | None = None


class RolOut(BaseModel):
    ID_Rol: int
    Nombre_Rol: str
    Descripcion: str | None = None
    permisos: list[int] = []

    class Config:
        from_attributes = True


class PermisoOut(BaseModel):
    ID_Permiso: int
    Nombre_Permiso: str
    Descripcion: str | None = None

    class Config:
        from_attributes = True
