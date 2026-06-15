from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Auditoria(Base):
    __tablename__ = "Auditoria"

    ID_Auditoria = Column("ID_Auditoria", Integer, primary_key=True, autoincrement=True)
    ID_Usuario = Column("ID_Usuario", Integer, ForeignKey("Usuarios.ID_Usuario"), nullable=True)
    Accion = Column("Accion", String(50), nullable=False)
    Tabla_Afectada = Column("Tabla_Afectada", String(50))
    ID_Registro_Afectado = Column("ID_Registro_Afectado", Integer)
    Detalle = Column("Detalle", Text)
    Direccion_IP = Column("Direccion_IP", String(45))
    Fecha_Hora = Column("Fecha_Hora", DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
