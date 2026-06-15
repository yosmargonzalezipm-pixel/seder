from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class MinisterioGrupo(Base):
    __tablename__ = "Ministerios_Grupos"

    ID_Grupo = Column("ID_Grupo", Integer, primary_key=True, autoincrement=True)
    Nombre_Grupo = Column("Nombre_Grupo", String(150), nullable=False)
    Descripcion = Column("Descripcion", Text)
    ID_Lider = Column("ID_Lider", Integer, ForeignKey("Miembros.ID_Miembro", ondelete="SET NULL"), nullable=True)

    lider = relationship("Miembro", foreign_keys=[ID_Lider])
    miembros = relationship("MiembroGrupo", back_populates="grupo", cascade="all, delete-orphan")


class MiembroGrupo(Base):
    __tablename__ = "Miembros_Grupos"

    ID_Miembro = Column("ID_Miembro", Integer, ForeignKey("Miembros.ID_Miembro", ondelete="CASCADE"), primary_key=True)
    ID_Grupo = Column("ID_Grupo", Integer, ForeignKey("Ministerios_Grupos.ID_Grupo", ondelete="CASCADE"), primary_key=True)
    Rol = Column("Rol", String(100), default="Integrante")

    miembro = relationship("Miembro", back_populates="grupos")
    grupo = relationship("MinisterioGrupo", back_populates="miembros")
