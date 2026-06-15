from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey, Table,
    Enum as SAEnum, CHAR
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


miembros_profesiones = Table(
    "Miembros_Profesiones", Base.metadata,
    Column("ID_Miembro", Integer, ForeignKey("Miembros.ID_Miembro", ondelete="CASCADE"), primary_key=True),
    Column("ID_Profesion", Integer, ForeignKey("Profesiones.ID_Profesion", ondelete="CASCADE"), primary_key=True),
)

miembros_oficios = Table(
    "Miembros_Oficios", Base.metadata,
    Column("ID_Miembro", Integer, ForeignKey("Miembros.ID_Miembro", ondelete="CASCADE"), primary_key=True),
    Column("ID_Oficio", Integer, ForeignKey("Oficios.ID_Oficio", ondelete="CASCADE"), primary_key=True),
)


class Miembro(Base):
    __tablename__ = "Miembros"

    ID_Miembro = Column("ID_Miembro", Integer, primary_key=True, autoincrement=True)
    ID_Iglesia = Column("ID_Iglesia", Integer, ForeignKey("Iglesias.ID_Iglesia"), nullable=False)
    Cedula = Column("Cedula", String(20), unique=True, nullable=False)
    Nombres = Column("Nombres", String(100), nullable=False)
    Apellidos = Column("Apellidos", String(100), nullable=False)
    Fecha_Nacimiento = Column("Fecha_Nacimiento", Date, nullable=True)
    Telefono = Column("Telefono", String(20), nullable=True)
    Correo_Electronico = Column("Correo_Electronico", String(100), nullable=True)
    Fecha_Bautismo = Column("Fecha_Bautismo", Date, nullable=True)
    Fecha_Conversion = Column("Fecha_Conversion", Date, nullable=True)
    Estado = Column(
        "Estado",
        SAEnum("Activo", "Inactivo", "Visitante", "Trasladado", "Excomulgado"),
        default="Visitante",
    )
    ID_Familia = Column("ID_Familia", Integer, ForeignKey("Familias.ID_Familia"), nullable=True)
    ID_Ciudad = Column("ID_Ciudad", Integer, ForeignKey("Ciudades.ID_Ciudad"), nullable=False)
    ID_Parroquia = Column("ID_Parroquia", Integer, ForeignKey("Parroquias.ID_Parroquia"), nullable=False)
    Direccion = Column("Direccion", Text, nullable=True)
    Sexo = Column("Sexo", CHAR(1), nullable=True)
    Estado_Civil = Column("Estado_Civil", String(50), nullable=True)
    Creado_En = Column("Creado_En", DateTime, default=datetime.utcnow)
    Actualizado_En = Column("Actualizado_En", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="miembro", uselist=False)
    iglesia = relationship("Iglesia")
    ciudad = relationship("Ciudad")
    parroquia = relationship("Parroquia")
    familia = relationship("Familia", foreign_keys=[ID_Familia])
    profesiones = relationship("Profesion", secondary=miembros_profesiones)
    oficios = relationship("Oficio", secondary=miembros_oficios)
    roles_eclesiasticos = relationship("MiembroRol", back_populates="miembro", cascade="all, delete-orphan")
    grupos = relationship("MiembroGrupo", back_populates="miembro", cascade="all, delete-orphan")


class MiembroRol(Base):
    __tablename__ = "Miembros_Roles"

    ID_Miembro = Column("ID_Miembro", Integer, ForeignKey("Miembros.ID_Miembro", ondelete="CASCADE"), primary_key=True)
    ID_Rol = Column("ID_Rol", Integer, ForeignKey("Roles.ID_Rol", ondelete="CASCADE"), primary_key=True)
    Fecha_Asignacion = Column("Fecha_Asignacion", Date, nullable=True)
    Estado_Rol = Column("Estado_Rol", SAEnum("Activo", "Inactivo"), default="Activo")

    miembro = relationship("Miembro", back_populates="roles_eclesiasticos")
    rol = relationship("Rol")
