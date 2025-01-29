from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Reports(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True)  # Primary key
    product_name = Column(String)
    brand_name = Column(String)
    social_media_platform = Column(String)
    post_url = Column(String)
    description = Column(String)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey('users.id'), nullable=True)  # User who verified the report

    # Relationships
    verified_by_user = relationship("User", back_populates="verified_reports")
    flaged_products = relationship("FlagedProducts", back_populates="report")
    

