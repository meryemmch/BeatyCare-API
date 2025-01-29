from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
import models.recognized_products
import models.flaged_products

search_router = APIRouter()

@search_router.get("/search_product_by_name", response_model=dict)
def search_product_by_name(product_name: str, db: Session = Depends(get_db)):
    if not product_name:
        raise HTTPException(status_code=400, detail="Product name must be provided.")
    
    recognized_product = db.query(models.recognized_products.RecognizedProducts).filter(
        models.recognized_products.RecognizedProducts.product_name == product_name).first()
    
    flagged_product = db.query(models.flaged_products.FlagedProducts).filter(
        models.flaged_products.FlagedProducts.product_name == product_name).first()

    return {
        "recognized": bool(recognized_product),
        "flagged": bool(flagged_product)
    }



@search_router.get("/search_product_by_brand", response_model=dict)
def search_product_by_brand(brand_name: str, db: Session = Depends(get_db)):
    if not brand_name:
        raise HTTPException(status_code=400, detail="Brand name must be provided.")
    
    flagged_products = db.query(models.flaged_products.FlagedProducts).join(
        models.reports.Reports, models.flaged_products.FlagedProducts.report_id == models.reports.Reports.report_id
    ).filter(models.reports.Reports.brand_name == brand_name).all()
    
    flagged_products_info = []
    for product in flagged_products:
        report_count = db.query(models.reports.Reports).filter(
            models.reports.Reports.product_name == product.product_name).count()
        flagged_products_info.append({
            "flaged_product_name": product.product_name,
            "number_of_reports": report_count
        })

    return {
        "flagged_products": flagged_products_info
    }


