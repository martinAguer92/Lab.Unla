from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from fastapi import HTTPException, status
import models, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""------------------------------------PRODUCTOS-----------------------------------------------"""

@app.post("/productos/", status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        existing_product =(
            db.query(models.Product).filter(models.Product.nombre==product.nombre).first()
            )
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exist"
            )
        new_product = models.Product(
            nombre=product.nombre, precio=product.precio
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {"product": new_product}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred with trying to create product {e}",
        )


@app.get("/productos/{product_id}", status_code=status.HTTP_200_OK)
def read_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product= db.query(models.Product).filter(models.Product.id==product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The product was not found"
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error ocurred with trying to read product {e}",
        )
        

@app.delete("/productos/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id:int, db: Session=Depends(get_db)):
    try:
        product =db.query(models.Product).filter(models.Product.id==product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "The product was not found"
            )
        db.delete(product)
        db.commit()
        return "The product was deleted successfully"
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to delete product: {e}"
        )


@app.put("/productos/{product_id}", status_code=status.HTTP_200_OK)
def modify_product(product_id: int,product_update: schemas.ProductCreate, db: Session=Depends(get_db)):
    try:
        product= db.query(models.Product).filter(models.Product.id == product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "The product was not found"
            )
        product.nombre = product_update.nombre
        product.precio = product_update.precio
        db.commit()
        db.refresh(product)
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to update product: {e}"
        )
    

"""------------------------------------VENTAS-----------------------------------------------"""

@app.post("/ventas/", status_code =status.HTTP_201_CREATED, response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate,  db: Session=Depends(get_db)):
    try:
        product_existing = db.query(models.Product).filter(models.Product.id ==sale.id_producto).first()
        if not product_existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product dosen't exist"
            )
        if sale.cantidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero"
            )
        new_sale = models.Sale(
            fecha=sale.fecha,
            hora=sale.hora,
            cantidad=sale.cantidad,
            id_producto=sale.id_producto,
            precio_total=sale.cantidad * product_existing.precio
        )

        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)

        return new_sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred with trying to create product {e}",
        )


@app.get("/ventas/{sale_id}", status_code=status.HTTP_200_OK, response_model=schemas.SaleResponse)
def read_sale (sale_id:int,db: Session=Depends(get_db)):
    try:
        sale=db.query(models.Sale).filter(models.Sale.id==sale_id).first()

        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale dosen't found"
            )
        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred with trying to read sale {e}"
        )

@app.delete("/ventas/{sale_id}", status_code=status.HTTP_200_OK)
def delete_sale (sale_id:int, db: Session=Depends(get_db)):
    try:
        sale=db.query(models.Sale).filter(models.Sale.id==sale_id).first()

        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="sale dosen't found"
            )
        db.delete(sale)
        db.commit()
        return "The sale was deleted successfully"
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred whit trying to delete sale {e}"
        ) 
    


@app.put("/ventas/{sale_id}", status_code=status.HTTP_200_OK, response_model=schemas.SaleResponse)
def modify_sale(sale_id:int, sale_update:schemas.SaleCreate, db: Session=Depends(get_db)):
    try:
        sale=db.query(models.Sale).filter(models.Sale.id==sale_id).first()

        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale dosen't found"
            )
        if sale_update.cantidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero"
            )
        product = db.query(models.Product).filter(models.Product.id ==sale_update.id_producto).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product dosen't exist"
                )
        
        sale.fecha =sale_update.fecha
        sale.hora =sale_update.hora
        sale.cantidad = sale_update.cantidad
        sale.id_producto = sale_update.id_producto
        sale.precio_total = sale.cantidad * product.precio
        
        db.commit()
        db.refresh(sale)
        return sale
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error ocurred with trying to modify sale {e}"
        )

"""------------------------------------CARRITO-----------------------------------------------"""
    