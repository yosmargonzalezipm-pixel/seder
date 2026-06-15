from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Miembro, Inventario
from app.utils.security import get_current_user, tiene_permiso
from app.models.usuario import Usuario
from app.reportes.excel import exportar_miembros_excel, exportar_inventario_excel
from app.reportes.pdf import exportar_miembros_pdf, exportar_inventario_pdf

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


@router.get("/miembros/excel")
def reporte_miembros_excel(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "reportes.exportar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembros = db.query(Miembro).order_by(Miembro.Apellidos).all()
    data = exportar_miembros_excel(miembros)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=miembros.xlsx"},
    )


@router.get("/inventario/excel")
def reporte_inventario_excel(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "reportes.exportar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    articulos = db.query(Inventario).order_by(Inventario.Nombre_Articulo).all()
    data = exportar_inventario_excel(articulos)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=inventario.xlsx"},
    )


@router.get("/miembros/pdf")
def reporte_miembros_pdf(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "reportes.exportar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembros = db.query(Miembro).order_by(Miembro.Apellidos).all()
    data = exportar_miembros_pdf(miembros)
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=miembros.pdf"},
    )


@router.get("/inventario/pdf")
def reporte_inventario_pdf(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "reportes.exportar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    articulos = db.query(Inventario).order_by(Inventario.Nombre_Articulo).all()
    data = exportar_inventario_pdf(articulos)
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=inventario.pdf"},
    )


@router.get("/miembros/preview")
def preview_miembros(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "reportes.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    miembros = db.query(Miembro).order_by(Miembro.ID_Miembro.desc()).limit(10).all()
    return [
        {
            "Cédula": m.Cedula,
            "Nombres": m.Nombres,
            "Apellidos": m.Apellidos,
            "Fecha_Nacimiento": str(m.Fecha_Nacimiento) if m.Fecha_Nacimiento else "",
            "Teléfono": m.Telefono or "",
            "Correo_Electrónico": m.Correo_Electronico or "",
            "Sexo": m.Sexo or "",
            "Estado_Civil": m.Estado_Civil or "",
            "Estado": m.Estado or "",
            "Fecha_Bautismo": str(m.Fecha_Bautismo) if m.Fecha_Bautismo else "",
            "Fecha_Conversión": str(m.Fecha_Conversion) if m.Fecha_Conversion else "",
            "Iglesia": m.iglesia.Nombre_Iglesia if m.iglesia else "",
            "Familia": m.familia.Nombre_Familia if m.familia else "",
            "Ciudad": m.ciudad.Nombre_Ciudad if m.ciudad else "",
            "Parroquia": m.parroquia.Nombre_Parroquia if m.parroquia else "",
            "Dirección": m.Direccion or "",
            "Profesiones": ", ".join(p.Nombre_Profesion for p in m.profesiones),
            "Oficios": ", ".join(o.Nombre_Oficio for o in m.oficios),
        }
        for m in miembros
    ]


@router.get("/inventario/preview")
def preview_inventario(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "reportes.ver", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    articulos = db.query(Inventario).order_by(Inventario.ID_Articulo.desc()).limit(10).all()
    return [
        {
            "Artículo": a.Nombre_Articulo,
            "Descripción": a.Descripcion or "",
            "Marca": a.Marca or "",
            "Modelo": a.Modelo or "",
            "N° Serie": a.Numero_Serie or "",
            "Cantidad": a.Cantidad,
            "Categoría": a.categoria.Nombre_Categoria if a.categoria else "",
            "Iglesia": a.iglesia.Nombre_Iglesia if a.iglesia else "",
            "Estado": a.Estado_Articulo,
            "Ubicación_Interna": a.Ubicacion_Interna or "",
            "Responsable": f"{a.miembro_resguarda.Nombres} {a.miembro_resguarda.Apellidos}" if a.miembro_resguarda else "",
            "Tipo_Ubicación": a.Tipo_Ubicacion,
            "Ubicación_Detallada": a.Ubicacion_Detallada or "",
        }
        for a in articulos
    ]
