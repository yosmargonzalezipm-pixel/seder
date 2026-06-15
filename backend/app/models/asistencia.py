from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class RegistroAsistencia(Base):
    __tablename__ = "Registro_Asistencia"

    ID_Asistencia = Column("ID_Asistencia", Integer, primary_key=True, autoincrement=True)
    ID_Miembro = Column("ID_Miembro", Integer, ForeignKey("Miembros.ID_Miembro"), nullable=False)
    Fecha = Column("Fecha", Date, nullable=False)
    Tipo_Evento = Column("Tipo_Evento", String(100), nullable=False)
    Estado_Asistencia = Column(
        "Estado_Asistencia",
        String(20),
        nullable=False,
    )
    Creado_En = Column("Creado_En", DateTime, default=datetime.utcnow)

    miembro = relationship("Miembro")
