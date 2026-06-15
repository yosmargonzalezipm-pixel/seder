import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Miembro, Iglesia, Inventario, CategoriaInventario
from app.utils.security import get_current_user, tiene_permiso
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/csv", tags=["CSV"])


def detectar_delimitador(cabecera: str) -> str:
    if "\t" in cabecera:
        return "\t"
    if ";" in cabecera:
        return ";"
    return ","


@router.post("/miembros")
def importar_miembros_csv(
    file: UploadFile = File(...),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "csv.importar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser .csv")

    content = file.file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content), delimiter=detectar_delimitador(content[:200]))

    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV vacío o sin cabeceras")

    importados = 0
    errores = []

    # Mapa de columnas esperadas
    col_map = {
        "cedula": "Cedula", "cédula": "Cedula", "Cedula": "Cedula",
        "nombres": "Nombres", "Nombres": "Nombres",
        "apellidos": "Apellidos", "Apellidos": "Apellidos",
        "telefono": "Telefono", "teléfono": "Telefono", "Telefono": "Telefono",
        "correo": "Correo_Electronico", "email": "Correo_Electronico",
        "sexo": "Sexo", "Sexo": "Sexo",
        "direccion": "Direccion", "dirección": "Direccion", "Direccion": "Direccion",
    }

    iglesia_id = db.query(Iglesia.ID_Iglesia).first()
    if not iglesia_id:
        raise HTTPException(status_code=400, detail="No hay iglesias registradas")
    iglesia_id = iglesia_id[0]

    for fila in reader:
        try:
            cedula = (fila.get("Cedula") or fila.get("cedula") or fila.get("cédula") or "").strip()
            if not cedula:
                errores.append(f"Fila sin cédula: {dict(fila)}")
                continue

            existe = db.query(Miembro).filter(Miembro.Cedula == cedula).first()
            if existe:
                errores.append(f"Cédula {cedula}: ya existe")
                continue

            nombres = (fila.get("Nombres") or fila.get("nombres") or "").strip()
            apellidos = (fila.get("Apellidos") or fila.get("apellidos") or "").strip()
            if not nombres or not apellidos:
                errores.append(f"Cédula {cedula}: faltan nombres o apellidos")
                continue

            telefono = (fila.get("Telefono") or fila.get("telefono") or "").strip() or None
            correo = (fila.get("Correo_Electronico") or fila.get("correo") or fila.get("email") or "").strip() or None
            sexo_str = (fila.get("Sexo") or fila.get("sexo") or "").strip().upper()
            sexo = sexo_str if sexo_str in ("M", "F") else None
            direccion = fila.get("Direccion") or fila.get("direccion") or None

            miembro = Miembro(
                ID_Iglesia=iglesia_id,
                Cedula=cedula,
                Nombres=nombres,
                Apellidos=apellidos,
                Telefono=telefono,
                Correo_Electronico=correo,
                Sexo=sexo,
                Direccion=direccion,
                ID_Ciudad=1,
                ID_Parroquia=1,
                Estado="Activo",
            )
            db.add(miembro)
            db.flush()
            importados += 1

        except Exception as e:
            errores.append(f"Error en fila: {str(e)}")

    db.commit()

    return {
        "importados": importados,
        "errores": errores,
        "total_filas": importados + len(errores),
    }


@router.post("/inventario")
def importar_inventario_csv(
    file: UploadFile = File(...),
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not tiene_permiso(usuario, "csv.importar", db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser .csv")

    content = file.file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content), delimiter=detectar_delimitador(content[:200]))

    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV vacío o sin cabeceras")

    importados = 0
    errores = []

    iglesia_id = db.query(Iglesia.ID_Iglesia).first()
    if not iglesia_id:
        raise HTTPException(status_code=400, detail="No hay iglesias registradas")
    iglesia_id = iglesia_id[0]

    for fila in reader:
        try:
            nombre = (fila.get("Nombre_Articulo") or fila.get("nombre") or fila.get("articulo") or "").strip()
            if not nombre:
                errores.append(f"Fila sin nombre de artículo: {dict(fila)}")
                continue

            categoria_nombre = fila.get("Categoria") or fila.get("categoria") or ""
            categoria = None
            if categoria_nombre:
                categoria = db.query(CategoriaInventario).filter(
                    CategoriaInventario.Nombre_Categoria.ilike(f"%{categoria_nombre.strip()}%")
                ).first()

            cantidad_str = fila.get("Cantidad") or fila.get("cantidad") or "1"
            try:
                cantidad = int(cantidad_str)
            except ValueError:
                cantidad = 1

            art = Inventario(
                ID_Iglesia=iglesia_id,
                ID_Categoria=categoria.ID_Categoria if categoria else 1,
                Nombre_Articulo=nombre,
                Marca=fila.get("Marca") or fila.get("marca") or None,
                Modelo=fila.get("Modelo") or fila.get("modelo") or None,
                Numero_Serie=fila.get("Numero_Serie") or fila.get("serie") or None,
                Cantidad=cantidad,
                Estado_Articulo="Bueno",
                Descripcion=fila.get("Descripcion") or None,
            )
            db.add(art)
            db.flush()
            importados += 1

        except Exception as e:
            errores.append(f"Error en fila: {str(e)}")

    db.commit()

    return {
        "importados": importados,
        "errores": errores,
        "total_filas": importados + len(errores),
    }
