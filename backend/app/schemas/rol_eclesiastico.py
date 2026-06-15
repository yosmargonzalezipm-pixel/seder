from datetime import date
from pydantic import BaseModel


class RolEclesiasticoCreate(BaseModel):
    Nombre_Rol: str
    Descripcion: str | None = None


class RolEclesiasticoUpdate(BaseModel):
    Nombre_Rol: str | None = None
    Descripcion: str | None = None


class RolEclesiasticoOut(BaseModel):
    ID_Rol: int
    Nombre_Rol: str
    Descripcion: str | None = None
    Total_Miembros: int = 0

    class Config:
        from_attributes = True


class MiembroRolAsignar(BaseModel):
    ID_Rol: int
    Fecha_Asignacion: date | None = None
    Estado_Rol: str = "Activo"


class MiembroRolOut(BaseModel):
    ID_Rol: int
    Nombre_Rol: str = ""
    Fecha_Asignacion: date | None = None
    Estado_Rol: str

    class Config:
        from_attributes = True
