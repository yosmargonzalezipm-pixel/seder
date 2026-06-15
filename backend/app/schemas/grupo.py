from pydantic import BaseModel


class GrupoCreate(BaseModel):
    Nombre_Grupo: str
    Descripcion: str | None = None
    ID_Lider: int | None = None


class GrupoUpdate(BaseModel):
    Nombre_Grupo: str | None = None
    Descripcion: str | None = None
    ID_Lider: int | None = None


class GrupoOut(BaseModel):
    ID_Grupo: int
    Nombre_Grupo: str
    Descripcion: str | None = None
    ID_Lider: int | None = None
    Lider_Nombre: str = ""
    Total_Miembros: int = 0

    class Config:
        from_attributes = True


class MiembroGrupoAsignar(BaseModel):
    ID_Miembro: int
    Rol: str = "Integrante"


class MiembroGrupoOut(BaseModel):
    ID_Miembro: int
    Miembro_Nombre: str = ""
    Rol: str = ""

    class Config:
        from_attributes = True
