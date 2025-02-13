from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from database.db import engine, SessionLocal
from database.db import get_db
import models.recognized_products
import models.flaged_products  
import models.reports
import models.users

verify_report_router = APIRouter()

class VerifyProduct:
    @staticmethod
    @verify_report_router.delete("/verify-product/auto-delete-recognized-reports", response_model=dict)
    async def delete_recognized_reports(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
        try:
            recognized_reports = db.query(models.reports.Reports).join(
                models.recognized_products.RecognizedProducts,
                (models.recognized_products.RecognizedProducts.product_name == models.reports.Reports.product_name) &
                (models.recognized_products.RecognizedProducts.brand_name == models.reports.Reports.brand_name)
            ).all()

            if not recognized_reports:
                return {"message": "No recognized reports found to delete."}

            for report in recognized_reports:
                db.delete(report)

            db.commit()
            return {"message": f"Deleted {len(recognized_reports)} recognized reports successfully."}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting recognized reports: {str(e)}")

    @staticmethod
    @verify_report_router.put("/verify-product/auto-verify-reports", response_model=dict)
    async def auto_verify_reports(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
        try:
        # Fetch all unverified reports
            unverified_reports = db.query(models.reports.Reports).filter(
            models.reports.Reports.is_verified == False
            ).all()

            if not unverified_reports:
               return {"message": "No unverified reports found."}

            verified_count = 0
            for report in unverified_reports:
            
                recognized_product = db.query(models.recognized_products.RecognizedProducts).filter(
                models.recognized_products.RecognizedProducts.product_name == report.product_name,
                models.recognized_products.RecognizedProducts.brand_name == report.brand_name
            ).first()

            if not recognized_product:
                report.is_verified = True  
                report.verified_by = current_user.username  
                verified_count += 1
            db.commit()
            return {"message": f"Verified {verified_count} reports successfully."}
        except Exception as e:
            db.rollback()
        raise HTTPException(status_code=500, detail=f"Error verifying reports: {str(e)}")


@staticmethod
@verify_report_router.post("/verify-product/add-flagged-products", response_model=dict)
async def add_verified_to_flagged(user_confirmation: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if user_confirmation.lower() != "yes":
        return {"message": "Operation cancelled by the user."}

    try:
        # Fetch all verified reports
        verified_reports = db.query(models.reports.Reports).filter(
            models.reports.Reports.is_verified == True
        ).all()

        # Check if there are any verified reports
        if not verified_reports:
            return {"message": "No verified reports to add to flagged products."}

        for report in verified_reports:
            # Check if the product already exists in the flagged products table
            flaged_product = db.query(models.flaged_products.FlagedProducts).filter(
                models.flaged_products.FlagedProducts.product_name == report.product_name,
            ).first()

            if flaged_product:
                # Skip increment logic if not necessary
                pass
            else:
                # Add a new flagged product and link it to the report
                new_flagged_product = models.flaged_products.FlagedProducts(
                    report_id=report.report_id, 
                    product_name=report.product_name,
                    number_of_reports=+1
                )
                db.add(new_flagged_product)

        db.commit()  # Commit once after processing all reports
        return {"message": "Verified reports added to flagged products successfully."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding verified reports to flagged products: {str(e)}")


