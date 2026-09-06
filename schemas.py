from pydantic import BaseModel

class ProductCreate(BaseModel):
    nombre: str
    precio: float

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True