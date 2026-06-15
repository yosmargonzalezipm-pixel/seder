"""
Script para crear el usuario administrador inicial.
Ejecutar: python seed_admin.py

Crea el usuario: admin / admin123
"""

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.security import hash_password


def seed_admin():
    db = SessionLocal()
    try:
        existe = db.query(Usuario).filter(Usuario.Nombre_Usuario == "admin").first()
        if existe:
            print("El usuario admin ya existe.")
            return

        admin = Usuario(
            Nombre_Usuario="admin",
            Email="admin@seder.local",
            Password_Hash=hash_password("admin123"),
            ID_Rol=1,
            Activo=True,
        )
        db.add(admin)
        db.commit()
        print("Usuario admin creado exitosamente.")
        print("  Usuario: admin")
        print("  Password: admin123")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
