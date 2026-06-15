from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Rol(Base):
    __tablename__ = "Roles"

    ID_Rol = Column("ID_Rol", Integer, primary_key=True, autoincrement=True)
    Nombre_Rol = Column("Nombre_Rol", String(100), nullable=False)
    Descripcion = Column("Descripcion", Text)

    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("RolPermiso", back_populates="rol")


class Permiso(Base):
    __tablename__ = "Permisos"

    ID_Permiso = Column("ID_Permiso", Integer, primary_key=True, autoincrement=True)
    Nombre_Permiso = Column("Nombre_Permiso", String(50), unique=True, nullable=False)
    Descripcion = Column("Descripcion", Text)

    roles = relationship("RolPermiso", back_populates="permiso")


class RolPermiso(Base):
    __tablename__ = "Roles_Permisos"

    ID_Rol = Column("ID_Rol", Integer, ForeignKey("Roles.ID_Rol"), primary_key=True)
    ID_Permiso = Column("ID_Permiso", Integer, ForeignKey("Permisos.ID_Permiso"), primary_key=True)

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")


class Usuario(Base):
    __tablename__ = "Usuarios"

    ID_Usuario = Column("ID_Usuario", Integer, primary_key=True, autoincrement=True)
    ID_Miembro = Column("ID_Miembro", Integer, ForeignKey("Miembros.ID_Miembro"), nullable=True)
    Nombre_Usuario = Column("Nombre_Usuario", String(50), unique=True, nullable=False)
    Email = Column("Email", String(100), unique=True, nullable=False)
    Password_Hash = Column("Password_Hash", String(255), nullable=False)
    ID_Rol = Column("ID_Rol", Integer, ForeignKey("Roles.ID_Rol"), nullable=False)
    Activo = Column("Activo", Boolean, default=True)
    Ultimo_Acceso = Column("Ultimo_Acceso", DateTime, nullable=True)
    Creado_En = Column("Creado_En", DateTime, default=datetime.utcnow)

    rol = relationship("Rol", back_populates="usuarios")
    miembro = relationship("Miembro", back_populates="usuario", uselist=False)
