from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi import HTTPException
import models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/productos/", response_model=schemas.ProductResponse)

def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Producto(nombre=product.nombre, precio=product.precio)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/productos/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.delete("/productos/{product_id}")
def delete_product(product_id: int, db: Session=Depends(get_db)):
    product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(product)
    db.commit()

    return {"detail": "Producto eliminado correctameente"}


@app.put("/productos/{product_id}",  response_model=schemas.ProductResponse)
def modifi_product(product: schemas.ProductCreate ,product_id: int, db: Session=Depends(get_db)):
    screatchProduct = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if screatchProduct is None:
        raise HTTPException(status_code=404,detail="Producto no encontrado")
    screatchProduct.nombre = product.nombre 
    screatchProduct.precio = product.precio
    
    db.commit()
    db.refresh(screatchProduct)
    return screatchProduct
