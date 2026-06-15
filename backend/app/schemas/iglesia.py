from datetime import datetime
from pydantic import BaseModel


class IglesiaCreate(BaseModel):
    Nombre_Iglesia: str
    ID_Iglesia_Madre: int | None = None
    Direccion: str
    Telefono_Iglesia_movil: str | None = None
    Telefono_fijo: str | None = None
    Correo: str | None = None
    ID_Ciudad: int
    ID_Parroquia: int


class IglesiaUpdate(BaseModel):
    Nombre_Iglesia: str | None = None
    ID_Iglesia_Madre: int | None = None
    Direccion: str | None = None
    Telefono_Iglesia_movil: str | None = None
    Telefono_fijo: str | None = None
    Correo: str | None = None
    ID_Ciudad: int | None = None
    ID_Parroquia: int | None = None


class IglesiaOut(BaseModel):
    ID_Iglesia: int
    Nombre_Iglesia: str
    ID_Iglesia_Madre: int | None = None
    Direccion: str
    Telefono_Iglesia_movil: str | None = None
    Telefono_fijo: str | None = None
    Correo: str | None = None
    ID_Ciudad: int
    ID_Parroquia: int
    Iglesia_Madre_Nombre: str = ""
    Ciudad_Nombre: str = ""
    Parroquia_Nombre: str = ""
    Creado_En: datetime | None = None
    Actualizado_En: datetime | None = None

    class Config:
        from_attributes = True
