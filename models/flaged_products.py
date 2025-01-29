from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class FlagedProducts(Base):
    __tablename__ = 'flaged_products'

    flaged_product_id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.report_id'), nullable=False)  # Reference to Reports
    product_name = Column(String, nullable=False)
    number_of_reports=Column(Integer, nullable=False)

    # Relationship to the Reports table
    report = relationship("Reports", back_populates="flaged_products")
