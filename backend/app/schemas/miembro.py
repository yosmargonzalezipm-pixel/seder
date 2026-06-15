from datetime import date
from pydantic import BaseModel


class MiembroCreate(BaseModel):
    ID_Iglesia: int
    Cedula: str
    Nombres: str
    Apellidos: str
    Fecha_Nacimiento: date | None = None
    Telefono: str | None = None
    Correo_Electronico: str | None = None
    Fecha_Bautismo: date | None = None
    Fecha_Conversion: date | None = None
    Estado: str = "Visitante"
    ID_Familia: int | None = None
    ID_Ciudad: int
    ID_Parroquia: int
    Direccion: str | None = None
    Sexo: str | None = None
    Estado_Civil: str | None = None


class MiembroUpdate(BaseModel):
    ID_Iglesia: int | None = None
    Cedula: str | None = None
    Nombres: str | None = None
    Apellidos: str | None = None
    Fecha_Nacimiento: date | None = None
    Telefono: str | None = None
    Correo_Electronico: str | None = None
    Fecha_Bautismo: date | None = None
    Fecha_Conversion: date | None = None
    Estado: str | None = None
    ID_Familia: int | None = None
    ID_Ciudad: int | None = None
    ID_Parroquia: int | None = None
    Direccion: str | None = None
    Sexo: str | None = None
    Estado_Civil: str | None = None


class MiembroOut(BaseModel):
    ID_Miembro: int
    ID_Iglesia: int
    Cedula: str
    Nombres: str
    Apellidos: str
    Fecha_Nacimiento: date | None = None
    Telefono: str | None = None
    Correo_Electronico: str | None = None
    Fecha_Bautismo: date | None = None
    Fecha_Conversion: date | None = None
    Estado: str
    ID_Familia: int | None = None
    ID_Ciudad: int
    ID_Parroquia: int
    Direccion: str | None = None
    Sexo: str | None = None
    Estado_Civil: str | None = None
    Profesiones: list[str] = []
    Oficios: list[str] = []

    class Config:
        from_attributes = True


class MiembroListOut(BaseModel):
    ID_Miembro: int
    Cedula: str
    Nombres: str
    Apellidos: str
    Telefono: str | None = None
    Correo_Electronico: str | None = None
    Sexo: str | None = None
    Estado_Civil: str | None = None
    Fecha_Nacimiento: date | None = None
    Estado: str
    Iglesia: str = ""
    Profesiones: list[str] = []
    Oficios: list[str] = []

    class Config:
        from_attributes = True
