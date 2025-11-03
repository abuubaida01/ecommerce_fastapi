from pydantic import BaseModel

class MyBase(BaseModel): 
  name: str 
  address_line1: str
  address_line2: str | None  = None 
  city: str 
  state: str 
  pin_code: str 
  country: str 
  



class Create(MyBase): 
  pass 


class Out(MyBase): 
  id: int
  user_id: int 
  model_config = {"from_attributes": True}


class Update(BaseModel): 
  name: str | None  = None
  address_line1: str | None  = None
  address_line2: str | None  = None 
  city: str | None  = None
  state: str | None  = None
  pin_code: str | None  = None
  country: str | None  = None