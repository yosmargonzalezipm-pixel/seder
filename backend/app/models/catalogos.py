from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.database import Base


class Pais(Base):
    __tablename__ = "Paises"
    ID_Pais = Column("ID_Pais", Integer, primary_key=True, autoincrement=True)
    Nombre_Pais = Column("Nombre_Pais", String(100), nullable=False)


class Estado(Base):
    __tablename__ = "Estados"
    ID_Estado = Column("ID_Estado", Integer, primary_key=True, autoincrement=True)
    Nombre_Estado = Column("Nombre_Estado", String(100), nullable=False)
    ID_Pais = Column("ID_Pais", Integer, ForeignKey("Paises.ID_Pais"), nullable=False)


class Municipio(Base):
    __tablename__ = "Municipios"
    ID_Municipio = Column("ID_Municipio", Integer, primary_key=True, autoincrement=True)
    Nombre_Municipio = Column("Nombre_Municipio", String(100), nullable=False)
    ID_Estado = Column("ID_Estado", Integer, ForeignKey("Estados.ID_Estado"), nullable=False)


class Parroquia(Base):
    __tablename__ = "Parroquias"
    ID_Parroquia = Column("ID_Parroquia", Integer, primary_key=True, autoincrement=True)
    Nombre_Parroquia = Column("Nombre_Parroquia", String(100), nullable=False)
    ID_Municipio = Column("ID_Municipio", Integer, ForeignKey("Municipios.ID_Municipio"), nullable=False)


class Ciudad(Base):
    __tablename__ = "Ciudades"
    ID_Ciudad = Column("ID_Ciudad", Integer, primary_key=True, autoincrement=True)
    Nombre_Ciudad = Column("Nombre_Ciudad", String(100), nullable=False)
    ID_Estado = Column("ID_Estado", Integer, ForeignKey("Estados.ID_Estado"), nullable=False)


class Profesion(Base):
    __tablename__ = "Profesiones"
    ID_Profesion = Column("ID_Profesion", Integer, primary_key=True, autoincrement=True)
    Nombre_Profesion = Column("Nombre_Profesion", String(100), nullable=False)


class Oficio(Base):
    __tablename__ = "Oficios"
    ID_Oficio = Column("ID_Oficio", Integer, primary_key=True, autoincrement=True)
    Nombre_Oficio = Column("Nombre_Oficio", String(100), nullable=False)


class CategoriaInventario(Base):
    __tablename__ = "Categorias_Inventario"
    ID_Categoria = Column("ID_Categoria", Integer, primary_key=True, autoincrement=True)
    Nombre_Categoria = Column("Nombre_Categoria", String(100), nullable=False)


class Iglesia(Base):
    __tablename__ = "Iglesias"
    ID_Iglesia = Column("ID_Iglesia", Integer, primary_key=True, autoincrement=True)
    Nombre_Iglesia = Column("Nombre_Iglesia", String(150), nullable=False)
    ID_Iglesia_Madre = Column("ID_Iglesia_Madre", Integer, ForeignKey("Iglesias.ID_Iglesia"), nullable=True)
    Direccion = Column("Direccion", Text, nullable=False)
    Telefono_Iglesia_movil = Column("Telefono_Iglesia_movil", String(20), nullable=True)
    Telefono_fijo = Column("Telefono_fijo", String(20), nullable=True)
    Correo = Column("Correo", String(100), nullable=True)
    ID_Ciudad = Column("ID_Ciudad", Integer, ForeignKey("Ciudades.ID_Ciudad"), nullable=False)
    ID_Parroquia = Column("ID_Parroquia", Integer, ForeignKey("Parroquias.ID_Parroquia"), nullable=False)
    Creado_En = Column("Creado_En", DateTime, default=datetime.utcnow)
    Actualizado_En = Column("Actualizado_En", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    iglesia_madre = relationship("Iglesia", remote_side="Iglesia.ID_Iglesia")
    ciudad = relationship("Ciudad")
    parroquia = relationship("Parroquia")


class Parentesco(Base):
    __tablename__ = "Parentescos"
    ID_Parentesco = Column("ID_Parentesco", Integer, primary_key=True, autoincrement=True)
    Nombre = Column("Nombre", String(100), nullable=False)


class Familia(Base):
    __tablename__ = "Familias"
    ID_Familia = Column("ID_Familia", Integer, primary_key=True, autoincrement=True)
    Nombre_Familia = Column("Nombre_Familia", String(150), nullable=False)
    ID_Cabeza_Familia = Column("ID_Cabeza_Familia", Integer, ForeignKey("Miembros.ID_Miembro"), nullable=True)
    cabeza_familia = relationship("Miembro", foreign_keys=[ID_Cabeza_Familia])
