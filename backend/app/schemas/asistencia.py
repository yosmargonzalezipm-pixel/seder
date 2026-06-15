from datetime import date
from pydantic import BaseModel


class AsistenciaCreate(BaseModel):
    ID_Miembro: int
    Fecha: date
    Tipo_Evento: str
    Estado_Asistencia: str


class AsistenciaUpdate(BaseModel):
    ID_Miembro: int | None = None
    Fecha: date | None = None
    Tipo_Evento: str | None = None
    Estado_Asistencia: str | None = None


class AsistenciaOut(BaseModel):
    ID_Asistencia: int
    ID_Miembro: int
    Fecha: date
    Tipo_Evento: str
    Estado_Asistencia: str
    Miembro_Nombre: str = ""

    class Config:
        from_attributes = True
