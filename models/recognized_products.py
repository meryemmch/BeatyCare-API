from sqlalchemy import Column ,Integer ,String
from database.db import Base


class RecognizedProducts(Base):
    __tablename__ = "recognized_products"
    product_id = Column(Integer,primary_key=True , index =True)
    product_name =Column(String(100), nullable=False)
    brand_name = Column(String(100), nullable=False)
    recognition_date = Column(String(100), nullable=False)
    origin = Column(String(100), nullable=False) 
    
