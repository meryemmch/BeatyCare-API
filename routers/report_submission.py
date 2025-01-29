from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
import models.reports
from schemas.report import ReportsSchema


report_submission_router = APIRouter()

@report_submission_router.post("/submit_report/", response_model=dict)
async def submit_report(report: ReportsSchema, db: Session = Depends(get_db)):
    try:
        new_report = models.reports.Reports(
            product_name=report.product_name,
            brand_name=report.brand_name,
            social_media_platform=report.social_media_platform,
            post_url=report.post_url,
            description=report.description
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return {"message": "Report submitted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting report: {str(e)}")