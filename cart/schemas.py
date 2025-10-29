from pydantic import BaseModel

class CartItemBase(BaseModel):
  product_id: int 
  quantity: int 

