import io
from datetime import datetime

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from app.models import Miembro, Inventario


def _build_pdf(title: str, headers: list[str], data: list[list[str]], font_size: int = 8) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(letter), leftMargin=20, rightMargin=20, topMargin=30, bottomMargin=20)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    table_data = [headers]
    table_data.extend(data)

    col_widths = [doc.width / len(headers)] * len(headers)
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTSIZE", (0, 1), (-1, -1), font_size),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    elements.append(table)
    doc.build(elements)
    buf.seek(0)
    return buf.read()


def exportar_miembros_pdf(miembros: list[Miembro]) -> bytes:
    headers = [
        "Cédula", "Nombres", "Apellidos", "F.Nac.", "Teléfono", "Correo",
        "Sexo", "Est.Civil", "Estado", "F.Baut.", "F.Conv.",
        "Iglesia", "Familia", "Ciudad", "Parroquia", "Dirección",
        "Profesiones", "Oficios",
    ]
    data = [
        [
            m.Cedula, m.Nombres, m.Apellidos,
            str(m.Fecha_Nacimiento) if m.Fecha_Nacimiento else "",
            m.Telefono or "", m.Correo_Electronico or "",
            m.Sexo or "", m.Estado_Civil or "", m.Estado,
            str(m.Fecha_Bautismo) if m.Fecha_Bautismo else "",
            str(m.Fecha_Conversion) if m.Fecha_Conversion else "",
            m.iglesia.Nombre_Iglesia if m.iglesia else "",
            m.familia.Nombre_Familia if m.familia else "",
            m.ciudad.Nombre_Ciudad if m.ciudad else "",
            m.parroquia.Nombre_Parroquia if m.parroquia else "",
            m.Direccion or "",
            ", ".join(p.Nombre_Profesion for p in m.profesiones),
            ", ".join(o.Nombre_Oficio for o in m.oficios),
        ]
        for m in miembros
    ]
    return _build_pdf("Reporte de Miembros", headers, data, font_size=7)


def exportar_inventario_pdf(articulos: list[Inventario]) -> bytes:
    headers = [
        "Artículo", "Descripción", "Marca", "Modelo", "N° Serie",
        "Cant.", "Categoría", "Iglesia", "Estado",
        "Ub.Int.", "Responsable", "Tipo_Ub.", "Ub.Detallada",
    ]
    data = [
        [
            a.Nombre_Articulo, a.Descripcion or "",
            a.Marca or "", a.Modelo or "", a.Numero_Serie or "",
            str(a.Cantidad),
            a.categoria.Nombre_Categoria if a.categoria else "",
            a.iglesia.Nombre_Iglesia if a.iglesia else "",
            a.Estado_Articulo,
            a.Ubicacion_Interna or "",
            f"{a.miembro_resguarda.Nombres} {a.miembro_resguarda.Apellidos}" if a.miembro_resguarda else "",
            a.Tipo_Ubicacion,
            a.Ubicacion_Detallada or "",
        ]
        for a in articulos
    ]
    return _build_pdf("Reporte de Inventario", headers, data, font_size=7)
