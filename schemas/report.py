from pydantic import BaseModel


class ReportsSchema(BaseModel):
    product_name: str
    brand_name: str
    social_media_platform: str
    post_url: str
    description: str

