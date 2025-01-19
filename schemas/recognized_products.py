from pydantic import BaseModel


class RecognizedProductSchema(BaseModel):
    product_id: int
    product_name: str
    brand_name: str
    recognition_date: str
    origin: str