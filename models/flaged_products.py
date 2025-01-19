from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class FlagedProducts(Base):
    __tablename__ = 'flaged_products'

    flaged_product_id = Column(Integer, primary_key=True)
    flaged_product_name = Column(String)
    brand_name = Column(String)
    number_of_reports = Column(Integer, default=0)
    report_id = Column(Integer, ForeignKey('reports.report_id'))  

    report = relationship("Reports", back_populates="flaged_products", foreign_keys=[report_id])
