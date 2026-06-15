from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grupos import MinisterioGrupo, MiembroGrupo
from app.models import Miembro
from app.schemas.grupo import GrupoCreate, GrupoUpdate, GrupoOut, MiembroGrupoOut
from app.utils.security import get_current_user, tiene_permiso
from app.utils.auditoria import registrar_auditoria
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/grupos", tags=["Grupos"])


@router.get("", response_model=list[GrupoOut])
def listar_grupos(
    q: str = Query(""),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    query = db.query(MinisterioGrupo)
    if q:
        query = query.filter(MinisterioGrupo.Nombre_Grupo.ilike(f"%{q}%"))
    grupos = query.order_by(MinisterioGrupo.Nombre_Grupo).all()
    return [
        GrupoOut(
            ID_Grupo=g.ID_Grupo,
            Nombre_Grupo=g.Nombre_Grupo,
            Descripcion=g.Descripcion,
            ID_Lider=g.ID_Lider,
            Lider_Nombre=f"{g.lider.Nombres} {g.lider.Apellidos}" if g.lider else "",
            Total_Miembros=len(g.miembros),
        )
        for g in grupos
    ]


@router.post("", response_model=GrupoOut, status_code=201)
def crear_grupo(
    data: GrupoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.crear", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    g = MinisterioGrupo(**data.model_dump())
    db.add(g)
    db.commit()
    db.refresh(g)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Ministerios", g.ID_Grupo, "Crear ministerio")
    db.commit()
    return GrupoOut(
        ID_Grupo=g.ID_Grupo,
        Nombre_Grupo=g.Nombre_Grupo,
        Descripcion=g.Descripcion,
        ID_Lider=g.ID_Lider,
        Lider_Nombre=f"{g.lider.Nombres} {g.lider.Apellidos}" if g.lider else "",
        Total_Miembros=0,
    )


@router.get("/{grupo_id}", response_model=GrupoOut)
def obtener_grupo(
    grupo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    g = db.query(MinisterioGrupo).filter(MinisterioGrupo.ID_Grupo == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return GrupoOut(
        ID_Grupo=g.ID_Grupo,
        Nombre_Grupo=g.Nombre_Grupo,
        Descripcion=g.Descripcion,
        ID_Lider=g.ID_Lider,
        Lider_Nombre=f"{g.lider.Nombres} {g.lider.Apellidos}" if g.lider else "",
        Total_Miembros=len(g.miembros),
    )


@router.put("/{grupo_id}", response_model=GrupoOut)
def actualizar_grupo(
    grupo_id: int,
    data: GrupoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    g = db.query(MinisterioGrupo).filter(MinisterioGrupo.ID_Grupo == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(g, key, val)
    db.commit()
    db.refresh(g)
    registrar_auditoria(db, usuario.ID_Usuario, "Actualizar", "Ministerios", g.ID_Grupo, "Actualizar ministerio")
    db.commit()
    return GrupoOut(
        ID_Grupo=g.ID_Grupo,
        Nombre_Grupo=g.Nombre_Grupo,
        Descripcion=g.Descripcion,
        ID_Lider=g.ID_Lider,
        Lider_Nombre=f"{g.lider.Nombres} {g.lider.Apellidos}" if g.lider else "",
        Total_Miembros=len(g.miembros),
    )


@router.delete("/{grupo_id}", status_code=204)
def eliminar_grupo(
    grupo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.eliminar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    g = db.query(MinisterioGrupo).filter(MinisterioGrupo.ID_Grupo == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    id_g = g.ID_Grupo
    db.delete(g)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Ministerios", id_g, "Eliminar ministerio")
    db.commit()

# --- Miembros del grupo ---


@router.get("/{grupo_id}/miembros", response_model=list[MiembroGrupoOut])
def listar_miembros_grupo(
    grupo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    g = db.query(MinisterioGrupo).filter(MinisterioGrupo.ID_Grupo == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return [
        MiembroGrupoOut(
            ID_Miembro=m.ID_Miembro,
            Miembro_Nombre=f"{m.miembro.Nombres} {m.miembro.Apellidos}" if m.miembro else "",
            Rol=m.Rol,
        )
        for m in g.miembros
    ]


@router.post("/{grupo_id}/miembros")
def agregar_miembro_grupo(
    grupo_id: int,
    data: dict,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    g = db.query(MinisterioGrupo).filter(MinisterioGrupo.ID_Grupo == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    miembro_id = data.get("ID_Miembro")
    if not miembro_id:
        raise HTTPException(status_code=400, detail="ID_Miembro requerido")
    miembro = db.query(Miembro).filter(Miembro.ID_Miembro == miembro_id).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    existe = db.query(MiembroGrupo).filter(MiembroGrupo.ID_Grupo == grupo_id, MiembroGrupo.ID_Miembro == miembro_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="El miembro ya está en el grupo")
    mg = MiembroGrupo(ID_Grupo=grupo_id, ID_Miembro=miembro_id, Rol=data.get("Rol", "Integrante"))
    db.add(mg)
    registrar_auditoria(db, usuario.ID_Usuario, "Crear", "Ministerios", grupo_id, f"Agregar miembro {miembro_id} a ministerio")
    db.commit()
    return {"mensaje": "Miembro agregado al grupo"}


@router.delete("/{grupo_id}/miembros/{miembro_id}", status_code=204)
def remover_miembro_grupo(
    grupo_id: int,
    miembro_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "ministerios.editar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
    mg = db.query(MiembroGrupo).filter(MiembroGrupo.ID_Grupo == grupo_id, MiembroGrupo.ID_Miembro == miembro_id).first()
    if not mg:
        raise HTTPException(status_code=404, detail="Miembro no está en el grupo")
    db.delete(mg)
    registrar_auditoria(db, usuario.ID_Usuario, "Eliminar", "Ministerios", grupo_id, f"Remover miembro {miembro_id} de ministerio")
    db.commit()
