from datetime import datetime
from pydantic import BaseModel


class AuditoriaOut(BaseModel):
    ID_Auditoria: int
    ID_Usuario: int | None = None
    Usuario_Nombre: str = ""
    Accion: str
    Tabla_Afectada: str | None = None
    ID_Registro_Afectado: int | None = None
    Detalle: str | None = None
    Direccion_IP: str | None = None
    Fecha_Hora: datetime | None = None

    class Config:
        from_attributes = True
