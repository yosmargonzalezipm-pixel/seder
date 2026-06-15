from pydantic import BaseModel


class CatalogoCreate(BaseModel):
    Nombre: str


class CatalogoUpdate(BaseModel):
    Nombre: str | None = None


class CatalogoOut(BaseModel):
    ID: int
    Nombre: str

    class Config:
        from_attributes = True


class MiembroProfesionesUpdate(BaseModel):
    profesiones: list[int] = []


class MiembroOficiosUpdate(BaseModel):
    oficios: list[int] = []
