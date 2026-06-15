from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Iglesia, CategoriaInventario, Ciudad, Parroquia, Familia
from app.models import Pais, Estado, Municipio
from app.schemas.comun import SelectOption
from app.utils.security import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/catalogos", tags=["Catálogos"])


@router.get("/iglesias", response_model=list[SelectOption])
def listar_iglesias(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return [SelectOption(value=i.ID_Iglesia, label=i.Nombre_Iglesia) for i in db.query(Iglesia).all()]


@router.get("/categorias", response_model=list[SelectOption])
def listar_categorias(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return [SelectOption(value=c.ID_Categoria, label=c.Nombre_Categoria) for c in db.query(CategoriaInventario).all()]


@router.get("/paises", response_model=list[SelectOption])
def listar_paises(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return [SelectOption(value=p.ID_Pais, label=p.Nombre_Pais) for p in db.query(Pais).all()]


@router.get("/estados", response_model=list[SelectOption])
def listar_estados(
    pais_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Estado)
    if pais_id:
        q = q.filter(Estado.ID_Pais == pais_id)
    return [SelectOption(value=e.ID_Estado, label=e.Nombre_Estado) for e in q.all()]


@router.get("/municipios", response_model=list[SelectOption])
def listar_municipios(
    estado_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Municipio)
    if estado_id:
        q = q.filter(Municipio.ID_Estado == estado_id)
    return [SelectOption(value=m.ID_Municipio, label=m.Nombre_Municipio) for m in q.all()]


@router.get("/ciudades", response_model=list[SelectOption])
def listar_ciudades(
    estado_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Ciudad)
    if estado_id:
        q = q.filter(Ciudad.ID_Estado == estado_id)
    return [SelectOption(value=c.ID_Ciudad, label=c.Nombre_Ciudad) for c in q.order_by(Ciudad.Nombre_Ciudad).all()]


@router.get("/parroquias", response_model=list[SelectOption])
def listar_parroquias(
    municipio_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Parroquia)
    if municipio_id:
        q = q.filter(Parroquia.ID_Municipio == municipio_id)
    return [SelectOption(value=p.ID_Parroquia, label=p.Nombre_Parroquia) for p in q.order_by(Parroquia.Nombre_Parroquia).all()]


@router.get("/familias", response_model=list[SelectOption])
def listar_familias(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return [SelectOption(value=f.ID_Familia, label=f.Nombre_Familia) for f in db.query(Familia).all()]
