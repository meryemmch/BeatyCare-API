from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
import models.recognized_products
import models.flaged_products

search_router = APIRouter()

@search_router.get("/search_product_by_name", response_model=dict)
def search_product_by_name(product_name: str, db: Session = Depends(get_db)):
    try:
        if not product_name:
            raise HTTPException(status_code=400, detail="Product name must be provided.")
        
        response = {}
        recognized_product = db.query(models.recognized_products.RecognizedProducts).filter(
            models.recognized_products.RecognizedProducts.product_name == product_name).first()
        flagged_product = db.query(models.flaged_products.FlagedProducts).filter(
            models.flaged_products.FlagedProducts.flaged_product_name == product_name).first()

        response["recognized"] = bool(recognized_product)
        response["flagged"] = bool(flagged_product)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for product by name: {str(e)}")


@search_router.get("/search_product_by_brand", response_model=dict)
def search_product_by_brand(brand_name: str, db: Session = Depends(get_db)):
    try:
        if not brand_name:
            raise HTTPException(status_code=400, detail="Brand name must be provided.")
        
        response = {}
        flagged_products = db.query(models.flaged_products.FlagedProducts).filter(
            models.flaged_products.FlagedProducts.brand_name == brand_name).all()

        if flagged_products:
            response["flagged_products"] = []
            for product in flagged_products:
                report_count = db.query(models.reports.Reports).filter(
                    models.reports.Reports.product_name == product.flaged_product_name).count()
                response["flagged_products"].append({
                    "flaged_product_name": product.flaged_product_name,
                    "number_of_reports": report_count
                })
        else:
            response["flagged_products"] = []

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for products by brand: {str(e)}")
