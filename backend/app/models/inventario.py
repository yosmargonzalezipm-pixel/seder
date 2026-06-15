from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, ForeignKey,
    Enum as SAEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Inventario(Base):
    __tablename__ = "Inventario"

    ID_Articulo = Column("ID_Articulo", Integer, primary_key=True, autoincrement=True)
    ID_Iglesia = Column("ID_Iglesia", Integer, ForeignKey("Iglesias.ID_Iglesia"), nullable=False)
    ID_Categoria = Column("ID_Categoria", Integer, ForeignKey("Categorias_Inventario.ID_Categoria"), nullable=False)
    Nombre_Articulo = Column("Nombre_Articulo", String(150), nullable=False)
    Descripcion = Column("Descripcion", Text, nullable=True)
    Marca = Column("Marca", String(100), nullable=True)
    Modelo = Column("Modelo", String(100), nullable=True)
    Numero_Serie = Column("Numero_Serie", String(100), nullable=True)
    Cantidad = Column("Cantidad", Integer, default=1, nullable=False)
    Estado_Articulo = Column(
        "Estado_Articulo",
        SAEnum("Excelente", "Bueno", "Requiere Mantenimiento", "Dañado"),
        default="Bueno",
    )
    Ubicacion_Interna = Column("Ubicacion_Interna", String(150), nullable=True)
    ID_Miembro_Resguarda = Column("ID_Miembro_Resguarda", Integer, ForeignKey("Miembros.ID_Miembro"), nullable=True)
    Tipo_Ubicacion = Column(
        "Tipo_Ubicacion",
        SAEnum("En el Templo", "En Resguardo Externo (Casa del miembro)", "En Tránsito"),
        default="En el Templo",
    )
    Ubicacion_Detallada = Column("Ubicacion_Detallada", Text, nullable=True)
    Creado_En = Column("Creado_En", DateTime, default=datetime.utcnow)
    Actualizado_En = Column("Actualizado_En", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    iglesia = relationship("Iglesia")
    categoria = relationship("CategoriaInventario")
    miembro_resguarda = relationship("Miembro")


class HistorialResguardo(Base):
    __tablename__ = "Historial_Resguardos"

    ID_Resguardo = Column("ID_Resguardo", Integer, primary_key=True, autoincrement=True)
    ID_Articulo = Column("ID_Articulo", Integer, ForeignKey("Inventario.ID_Articulo"), nullable=False)
    ID_Miembro_Responsable = Column("ID_Miembro_Responsable", Integer, ForeignKey("Miembros.ID_Miembro"), nullable=False)
    Fecha_Salida_Asignacion = Column("Fecha_Salida_Asignacion", DateTime, default=datetime.utcnow, nullable=False)
    Fecha_Devolucion_Prevista = Column("Fecha_Devolucion_Prevista", Date, nullable=True)
    Fecha_Devolucion_Real = Column("Fecha_Devolucion_Real", DateTime, nullable=True)
    Estado_Entrega = Column("Estado_Entrega", String(100), nullable=False)
    Estado_Devolucion = Column("Estado_Devolucion", String(100), nullable=True)
    Notas_Observaciones = Column("Notas_Observaciones", Text, nullable=True)

    articulo = relationship("Inventario")
    miembro_responsable = relationship("Miembro")
