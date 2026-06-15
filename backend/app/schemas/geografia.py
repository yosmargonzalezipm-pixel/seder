from pydantic import BaseModel
from typing import Optional


class PaisCreate(BaseModel):
    Nombre_Pais: str


class PaisUpdate(BaseModel):
    Nombre_Pais: Optional[str] = None


class PaisOut(BaseModel):
    ID_Pais: int
    Nombre_Pais: str

    class Config:
        from_attributes = True


class EstadoCreate(BaseModel):
    Nombre_Estado: str
    ID_Pais: int


class EstadoUpdate(BaseModel):
    Nombre_Estado: Optional[str] = None
    ID_Pais: Optional[int] = None


class EstadoOut(BaseModel):
    ID_Estado: int
    Nombre_Estado: str
    ID_Pais: int
    Pais_Nombre: str

    class Config:
        from_attributes = True


class MunicipioCreate(BaseModel):
    Nombre_Municipio: str
    ID_Estado: int


class MunicipioUpdate(BaseModel):
    Nombre_Municipio: Optional[str] = None
    ID_Estado: Optional[int] = None


class MunicipioOut(BaseModel):
    ID_Municipio: int
    Nombre_Municipio: str
    ID_Estado: int
    Estado_Nombre: str

    class Config:
        from_attributes = True


class CiudadCreate(BaseModel):
    Nombre_Ciudad: str
    ID_Estado: int


class CiudadUpdate(BaseModel):
    Nombre_Ciudad: Optional[str] = None
    ID_Estado: Optional[int] = None


class CiudadOut(BaseModel):
    ID_Ciudad: int
    Nombre_Ciudad: str
    ID_Estado: int
    Estado_Nombre: str

    class Config:
        from_attributes = True


class ParroquiaCreate(BaseModel):
    Nombre_Parroquia: str
    ID_Municipio: int


class ParroquiaUpdate(BaseModel):
    Nombre_Parroquia: Optional[str] = None
    ID_Municipio: Optional[int] = None


class ParroquiaOut(BaseModel):
    ID_Parroquia: int
    Nombre_Parroquia: str
    ID_Municipio: int
    Municipio_Nombre: str

    class Config:
        from_attributes = True
