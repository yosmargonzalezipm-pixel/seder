from sqlalchemy.orm import Session
from app.models.auditoria import Auditoria


def registrar_auditoria(
    db: Session,
    id_usuario: int,
    accion: str,
    tabla: str,
    id_registro: int = None,
    detalle: str = None,
):
    registro = Auditoria(
        ID_Usuario=id_usuario,
        Accion=accion,
        Tabla_Afectada=tabla,
        ID_Registro_Afectado=id_registro,
        Detalle=detalle,
        Direccion_IP="0.0.0.0",
    )
    db.add(registro)
