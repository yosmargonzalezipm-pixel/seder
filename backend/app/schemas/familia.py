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

    class Config:
        from_attributes = True
