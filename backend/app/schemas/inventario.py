from pydantic import BaseModel


class InventarioCreate(BaseModel):
    ID_Iglesia: int
    ID_Categoria: int
    Nombre_Articulo: str
    Descripcion: str | None = None
    Marca: str | None = None
    Modelo: str | None = None
    Numero_Serie: str | None = None
    Cantidad: int = 1
    Estado_Articulo: str = "Bueno"
    Ubicacion_Interna: str | None = None
    ID_Miembro_Resguarda: int | None = None
    Tipo_Ubicacion: str = "En el Templo"
    Ubicacion_Detallada: str | None = None


class InventarioUpdate(BaseModel):
    ID_Iglesia: int | None = None
    ID_Categoria: int | None = None
    Nombre_Articulo: str | None = None
    Descripcion: str | None = None
    Marca: str | None = None
    Modelo: str | None = None
    Numero_Serie: str | None = None
    Cantidad: int | None = None
    Estado_Articulo: str | None = None
    Ubicacion_Interna: str | None = None
    ID_Miembro_Resguarda: int | None = None
    Tipo_Ubicacion: str | None = None
    Ubicacion_Detallada: str | None = None


class InventarioOut(BaseModel):
    ID_Articulo: int
    ID_Iglesia: int
    ID_Categoria: int
    Nombre_Articulo: str
    Descripcion: str | None = None
    Marca: str | None = None
    Modelo: str | None = None
    Numero_Serie: str | None = None
    Cantidad: int
    Estado_Articulo: str
    Ubicacion_Interna: str | None = None
    ID_Miembro_Resguarda: int | None = None
    Tipo_Ubicacion: str
    Ubicacion_Detallada: str | None = None

    class Config:
        from_attributes = True


class InventarioListOut(BaseModel):
    ID_Articulo: int
    Nombre_Articulo: str
    Marca: str | None = None
    Modelo: str | None = None
    Numero_Serie: str | None = None
    Cantidad: int
    Estado_Articulo: str
    Tipo_Ubicacion: str
    Categoria: str = ""
    Iglesia: str = ""

    class Config:
        from_attributes = True
