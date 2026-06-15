from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.catalogos import Pais, Estado, Municipio, Ciudad, Parroquia
from app.schemas.geografia import (
    PaisCreate, PaisUpdate, PaisOut,
    EstadoCreate, EstadoUpdate, EstadoOut,
    MunicipioCreate, MunicipioUpdate, MunicipioOut,
    CiudadCreate, CiudadUpdate, CiudadOut,
    ParroquiaCreate, ParroquiaUpdate, ParroquiaOut,
)
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/geografia", tags=["Geografía"])

# --- Países ---

@router.get("/paises", response_model=list[PaisOut])
def listar_paises(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Pais)
    if q:
        query = query.filter(Pais.Nombre_Pais.ilike(f"%{q}%"))
    return query.order_by(Pais.Nombre_Pais).all()


@router.get("/paises/{pais_id}", response_model=PaisOut)
def obtener_pais(
    pais_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Pais).filter(Pais.ID_Pais == pais_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return p


@router.post("/paises", response_model=PaisOut, status_code=201)
def crear_pais(
    data: PaisCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = Pais(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Geografía", p.ID_Pais, "Crear país")
    db.commit()
    return p


@router.put("/paises/{pais_id}", response_model=PaisOut)
def actualizar_pais(
    pais_id: int,
    data: PaisUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Pais).filter(Pais.ID_Pais == pais_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="País no encontrado")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(p, key, val)
    db.commit()
    db.refresh(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Geografía", p.ID_Pais, "Actualizar país")
    db.commit()
    return p


@router.delete("/paises/{pais_id}", status_code=204)
def eliminar_pais(
    pais_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Pais).filter(Pais.ID_Pais == pais_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="País no encontrado")
    id_p = p.ID_Pais
    db.delete(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Geografía", id_p, "Eliminar país")
    db.commit()


# --- Estados ---

@router.get("/estados", response_model=list[EstadoOut])
def listar_estados(
    q: str = Query(""),
    pais_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Estado, Pais.Nombre_Pais).join(Pais, Estado.ID_Pais == Pais.ID_Pais)
    if q:
        query = query.filter(Estado.Nombre_Estado.ilike(f"%{q}%"))
    if pais_id:
        query = query.filter(Estado.ID_Pais == pais_id)
    rows = query.order_by(Estado.Nombre_Estado).all()
    return [EstadoOut(ID_Estado=e.ID_Estado, Nombre_Estado=e.Nombre_Estado, ID_Pais=e.ID_Pais, Pais_Nombre=pais_nombre) for e, pais_nombre in rows]


@router.get("/estados/{estado_id}", response_model=EstadoOut)
def obtener_estado(
    estado_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    row = db.query(Estado, Pais.Nombre_Pais).join(Pais).filter(Estado.ID_Estado == estado_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    e, pais_nombre = row
    return EstadoOut(ID_Estado=e.ID_Estado, Nombre_Estado=e.Nombre_Estado, ID_Pais=e.ID_Pais, Pais_Nombre=pais_nombre)


@router.post("/estados", response_model=EstadoOut, status_code=201)
def crear_estado(
    data: EstadoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    e = Estado(**data.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Geografía", e.ID_Estado, "Crear estado")
    db.commit()
    pais = db.query(Pais).filter(Pais.ID_Pais == e.ID_Pais).first()
    return EstadoOut(ID_Estado=e.ID_Estado, Nombre_Estado=e.Nombre_Estado, ID_Pais=e.ID_Pais, Pais_Nombre=pais.Nombre_Pais if pais else "")


@router.put("/estados/{estado_id}", response_model=EstadoOut)
def actualizar_estado(
    estado_id: int,
    data: EstadoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    e = db.query(Estado).filter(Estado.ID_Estado == estado_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(e, key, val)
    db.commit()
    db.refresh(e)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Geografía", e.ID_Estado, "Actualizar estado")
    db.commit()
    pais = db.query(Pais).filter(Pais.ID_Pais == e.ID_Pais).first()
    return EstadoOut(ID_Estado=e.ID_Estado, Nombre_Estado=e.Nombre_Estado, ID_Pais=e.ID_Pais, Pais_Nombre=pais.Nombre_Pais if pais else "")


@router.delete("/estados/{estado_id}", status_code=204)
def eliminar_estado(
    estado_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    e = db.query(Estado).filter(Estado.ID_Estado == estado_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    id_e = e.ID_Estado
    db.delete(e)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Geografía", id_e, "Eliminar estado")
    db.commit()


# --- Municipios ---

@router.get("/municipios", response_model=list[MunicipioOut])
def listar_municipios(
    q: str = Query(""),
    estado_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Municipio, Estado.Nombre_Estado).join(Estado, Municipio.ID_Estado == Estado.ID_Estado)
    if q:
        query = query.filter(Municipio.Nombre_Municipio.ilike(f"%{q}%"))
    if estado_id:
        query = query.filter(Municipio.ID_Estado == estado_id)
    rows = query.order_by(Municipio.Nombre_Municipio).all()
    return [MunicipioOut(ID_Municipio=m.ID_Municipio, Nombre_Municipio=m.Nombre_Municipio, ID_Estado=m.ID_Estado, Estado_Nombre=estado_nombre) for m, estado_nombre in rows]


@router.get("/municipios/{municipio_id}", response_model=MunicipioOut)
def obtener_municipio(
    municipio_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    row = db.query(Municipio, Estado.Nombre_Estado).join(Estado).filter(Municipio.ID_Municipio == municipio_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    m, estado_nombre = row
    return MunicipioOut(ID_Municipio=m.ID_Municipio, Nombre_Municipio=m.Nombre_Municipio, ID_Estado=m.ID_Estado, Estado_Nombre=estado_nombre)


@router.post("/municipios", response_model=MunicipioOut, status_code=201)
def crear_municipio(
    data: MunicipioCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = Municipio(**data.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Geografía", m.ID_Municipio, "Crear municipio")
    db.commit()
    estado = db.query(Estado).filter(Estado.ID_Estado == m.ID_Estado).first()
    return MunicipioOut(ID_Municipio=m.ID_Municipio, Nombre_Municipio=m.Nombre_Municipio, ID_Estado=m.ID_Estado, Estado_Nombre=estado.Nombre_Estado if estado else "")


@router.put("/municipios/{municipio_id}", response_model=MunicipioOut)
def actualizar_municipio(
    municipio_id: int,
    data: MunicipioUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = db.query(Municipio).filter(Municipio.ID_Municipio == municipio_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(m, key, val)
    db.commit()
    db.refresh(m)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Geografía", m.ID_Municipio, "Actualizar municipio")
    db.commit()
    estado = db.query(Estado).filter(Estado.ID_Estado == m.ID_Estado).first()
    return MunicipioOut(ID_Municipio=m.ID_Municipio, Nombre_Municipio=m.Nombre_Municipio, ID_Estado=m.ID_Estado, Estado_Nombre=estado.Nombre_Estado if estado else "")


@router.delete("/municipios/{municipio_id}", status_code=204)
def eliminar_municipio(
    municipio_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    m = db.query(Municipio).filter(Municipio.ID_Municipio == municipio_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    id_m = m.ID_Municipio
    db.delete(m)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Geografía", id_m, "Eliminar municipio")
    db.commit()


# --- Ciudades ---

@router.get("/ciudades", response_model=list[CiudadOut])
def listar_ciudades(
    q: str = Query(""),
    estado_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Ciudad, Estado.Nombre_Estado).join(Estado, Ciudad.ID_Estado == Estado.ID_Estado)
    if q:
        query = query.filter(Ciudad.Nombre_Ciudad.ilike(f"%{q}%"))
    if estado_id:
        query = query.filter(Ciudad.ID_Estado == estado_id)
    rows = query.order_by(Ciudad.Nombre_Ciudad).all()
    return [CiudadOut(ID_Ciudad=c.ID_Ciudad, Nombre_Ciudad=c.Nombre_Ciudad, ID_Estado=c.ID_Estado, Estado_Nombre=estado_nombre) for c, estado_nombre in rows]


@router.get("/ciudades/{ciudad_id}", response_model=CiudadOut)
def obtener_ciudad(
    ciudad_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    row = db.query(Ciudad, Estado.Nombre_Estado).join(Estado).filter(Ciudad.ID_Ciudad == ciudad_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    c, estado_nombre = row
    return CiudadOut(ID_Ciudad=c.ID_Ciudad, Nombre_Ciudad=c.Nombre_Ciudad, ID_Estado=c.ID_Estado, Estado_Nombre=estado_nombre)


@router.post("/ciudades", response_model=CiudadOut, status_code=201)
def crear_ciudad(
    data: CiudadCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = Ciudad(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Geografía", c.ID_Ciudad, "Crear ciudad")
    db.commit()
    estado = db.query(Estado).filter(Estado.ID_Estado == c.ID_Estado).first()
    return CiudadOut(ID_Ciudad=c.ID_Ciudad, Nombre_Ciudad=c.Nombre_Ciudad, ID_Estado=c.ID_Estado, Estado_Nombre=estado.Nombre_Estado if estado else "")


@router.put("/ciudades/{ciudad_id}", response_model=CiudadOut)
def actualizar_ciudad(
    ciudad_id: int,
    data: CiudadUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = db.query(Ciudad).filter(Ciudad.ID_Ciudad == ciudad_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(c, key, val)
    db.commit()
    db.refresh(c)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Geografía", c.ID_Ciudad, "Actualizar ciudad")
    db.commit()
    estado = db.query(Estado).filter(Estado.ID_Estado == c.ID_Estado).first()
    return CiudadOut(ID_Ciudad=c.ID_Ciudad, Nombre_Ciudad=c.Nombre_Ciudad, ID_Estado=c.ID_Estado, Estado_Nombre=estado.Nombre_Estado if estado else "")


@router.delete("/ciudades/{ciudad_id}", status_code=204)
def eliminar_ciudad(
    ciudad_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    c = db.query(Ciudad).filter(Ciudad.ID_Ciudad == ciudad_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    id_c = c.ID_Ciudad
    db.delete(c)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Geografía", id_c, "Eliminar ciudad")
    db.commit()


# --- Parroquias ---

@router.get("/parroquias", response_model=list[ParroquiaOut])
def listar_parroquias(
    q: str = Query(""),
    municipio_id: int | None = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(Parroquia, Municipio.Nombre_Municipio).join(Municipio, Parroquia.ID_Municipio == Municipio.ID_Municipio)
    if q:
        query = query.filter(Parroquia.Nombre_Parroquia.ilike(f"%{q}%"))
    if municipio_id:
        query = query.filter(Parroquia.ID_Municipio == municipio_id)
    rows = query.order_by(Parroquia.Nombre_Parroquia).all()
    return [ParroquiaOut(ID_Parroquia=p.ID_Parroquia, Nombre_Parroquia=p.Nombre_Parroquia, ID_Municipio=p.ID_Municipio, Municipio_Nombre=mun_nombre) for p, mun_nombre in rows]


@router.get("/parroquias/{parroquia_id}", response_model=ParroquiaOut)
def obtener_parroquia(
    parroquia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    row = db.query(Parroquia, Municipio.Nombre_Municipio).join(Municipio).filter(Parroquia.ID_Parroquia == parroquia_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    p, mun_nombre = row
    return ParroquiaOut(ID_Parroquia=p.ID_Parroquia, Nombre_Parroquia=p.Nombre_Parroquia, ID_Municipio=p.ID_Municipio, Municipio_Nombre=mun_nombre)


@router.post("/parroquias", response_model=ParroquiaOut, status_code=201)
def crear_parroquia(
    data: ParroquiaCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = Parroquia(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Geografía", p.ID_Parroquia, "Crear parroquia")
    db.commit()
    mun = db.query(Municipio).filter(Municipio.ID_Municipio == p.ID_Municipio).first()
    return ParroquiaOut(ID_Parroquia=p.ID_Parroquia, Nombre_Parroquia=p.Nombre_Parroquia, ID_Municipio=p.ID_Municipio, Municipio_Nombre=mun.Nombre_Municipio if mun else "")


@router.put("/parroquias/{parroquia_id}", response_model=ParroquiaOut)
def actualizar_parroquia(
    parroquia_id: int,
    data: ParroquiaUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Parroquia).filter(Parroquia.ID_Parroquia == parroquia_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(p, key, val)
    db.commit()
    db.refresh(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Geografía", p.ID_Parroquia, "Actualizar parroquia")
    db.commit()
    mun = db.query(Municipio).filter(Municipio.ID_Municipio == p.ID_Municipio).first()
    return ParroquiaOut(ID_Parroquia=p.ID_Parroquia, Nombre_Parroquia=p.Nombre_Parroquia, ID_Municipio=p.ID_Municipio, Municipio_Nombre=mun.Nombre_Municipio if mun else "")


@router.delete("/parroquias/{parroquia_id}", status_code=204)
def eliminar_parroquia(
    parroquia_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "geografia.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    p = db.query(Parroquia).filter(Parroquia.ID_Parroquia == parroquia_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Parroquia no encontrada")
    id_p = p.ID_Parroquia
    db.delete(p)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Geografía", id_p, "Eliminar parroquia")
    db.commit()
