from pydantic import BaseModel, ConfigDict
from datetime import date, time

class ProductCreate(BaseModel):
    nombre: str
    precio: float
    
    

class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SaleCreate(BaseModel):
    fecha: date
    hora: time
    cantidad: int
    id_producto : int

    

class SaleResponse(SaleCreate):
    id: int
    precio_total: float

    
    model_config = ConfigDict(from_attributes=True)

