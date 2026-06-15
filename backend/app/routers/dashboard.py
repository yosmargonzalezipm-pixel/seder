from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Miembro, Inventario, Familia, Iglesia, MinisterioGrupo
from app.models.asistencia import RegistroAsistencia
from app.utils.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total_miembros = db.query(func.count(Miembro.ID_Miembro)).scalar() or 0

    miembros_sexo = db.query(Miembro.Sexo, func.count(Miembro.ID_Miembro)).group_by(Miembro.Sexo).all()
    miembros_estado = db.query(Miembro.Estado, func.count(Miembro.ID_Miembro)).group_by(Miembro.Estado).all()

    total_inventario = db.query(func.count(Inventario.ID_Articulo)).scalar() or 0
    total_items = db.query(func.sum(Inventario.Cantidad)).scalar() or 0

    inventario_estado = db.query(Inventario.Estado_Articulo, func.count(Inventario.ID_Articulo)).group_by(Inventario.Estado_Articulo).all()

    total_familias = db.query(func.count(Familia.ID_Familia)).scalar() or 0
    total_iglesias = db.query(func.count(Iglesia.ID_Iglesia)).scalar() or 0
    total_grupos = db.query(func.count(MinisterioGrupo.ID_Grupo)).scalar() or 0
    total_asistencias = db.query(func.count(RegistroAsistencia.ID_Asistencia)).scalar() or 0

    return {
        "miembros": {
            "total": total_miembros,
            "por_sexo": {s or "Sin registro": c for s, c in miembros_sexo},
            "por_estado": {s or "Sin registro": c for s, c in miembros_estado},
        },
        "inventario": {
            "total_articulos": total_inventario,
            "total_items": int(total_items),
            "por_estado": {s or "Sin registro": c for s, c in inventario_estado},
        },
        "familias": {"total": total_familias},
        "iglesias": {"total": total_iglesias},
        "grupos": {"total": total_grupos},
        "asistencia": {"total": total_asistencias},
    }
