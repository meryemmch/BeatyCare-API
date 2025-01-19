from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
import models.recognized_products
from schemas.recognized_products import RecognizedProductSchema 

recognized_products_router = APIRouter()

@recognized_products_router.get("/recognized_products", response_model=list[RecognizedProductSchema])
def get_recognized_products(db: Session = Depends(get_db)):
    try:
        products = db.query(models.recognized_products.RecognizedProducts).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recognized products: {str(e)}")

@recognized_products_router.post("/recognized_products", response_model=RecognizedProductSchema)
def add_recognized_product(product: RecognizedProductSchema, db: Session = Depends(get_db)):
    try:
        new_product = models.recognized_products.RecognizedProducts(
            product_name=product.product_name,
            brand_name=product.brand_name,
            recognition_date=product.recognition_date,
            origin=product.origin
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding recognized product: {str(e)}")
