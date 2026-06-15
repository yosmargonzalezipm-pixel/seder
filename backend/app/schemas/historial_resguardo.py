from pydantic import BaseModel
from datetime import datetime, date


class HistorialResguardoCreate(BaseModel):
    ID_Articulo: int
    ID_Miembro_Responsable: int
    Fecha_Salida_Asignacion: datetime | None = None
    Fecha_Devolucion_Prevista: date | None = None
    Estado_Entrega: str = "Entregado"
    Estado_Devolucion: str | None = None
    Notas_Observaciones: str | None = None


class HistorialResguardoUpdate(BaseModel):
    ID_Articulo: int | None = None
    ID_Miembro_Responsable: int | None = None
    Fecha_Salida_Asignacion: datetime | None = None
    Fecha_Devolucion_Prevista: date | None = None
    Estado_Entrega: str | None = None
    Estado_Devolucion: str | None = None
    Notas_Observaciones: str | None = None


class HistorialResguardoOut(BaseModel):
    ID_Resguardo: int
    ID_Articulo: int
    ID_Miembro_Responsable: int
    Fecha_Salida_Asignacion: datetime | None = None
    Fecha_Devolucion_Prevista: date | None = None
    Fecha_Devolucion_Real: datetime | None = None
    Estado_Entrega: str
    Estado_Devolucion: str | None = None
    Notas_Observaciones: str | None = None
    Creado_En: datetime | None = None
    Actualizado_En: datetime | None = None

    class Config:
        from_attributes = True


class HistorialResguardoListOut(BaseModel):
    ID_Resguardo: int
    ID_Articulo: int
    Nombre_Articulo: str = ""
    ID_Miembro_Responsable: int
    Nombre_Miembro: str = ""
    Fecha_Salida_Asignacion: datetime | None = None
    Fecha_Devolucion_Prevista: date | None = None
    Estado_Entrega: str
    Estado_Devolucion: str | None = None

    class Config:
        from_attributes = True
