from pydantic import BaseModel


class FamiliaCreate(BaseModel):
    Nombre_Familia: str
    ID_Cabeza_Familia: int | None = None


class FamiliaUpdate(BaseModel):
    Nombre_Familia: str | None = None
    ID_Cabeza_Familia: int | None = None


class FamiliaOut(BaseModel):
    ID_Familia: int
    Nombre_Familia: str
    ID_Cabeza_Familia: int | None = None
    Cabeza_Familia_Nombre: str | None = None
    Num_Miembros: int = 0

    class Config:
        from_attributes = True


class AsignarMiembroBody(BaseModel):
    ID_Parentesco: int | None = None
