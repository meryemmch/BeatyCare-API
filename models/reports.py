from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.db import Base

class Reports(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    brand_name = Column(String)
    social_media_platform = Column(String)
    post_url = Column(String)
    author_name = Column(String)
    description = Column(String)
    is_verified = Column(Boolean, default=False)
    
    flaged_products = relationship("FlagedProducts", back_populates="report")
