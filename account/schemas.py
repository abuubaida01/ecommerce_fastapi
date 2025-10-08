from pydantic import BaseModel, EmailStr

class UserBase(BaseModel): 
  email: EmailStr
  is_active: bool
  is_admin: bool
  is_verified: bool

class UserCreate(UserBase): 
  password: str


class UserOut(UserBase):
  id: int
  model_config = {"from_attributes": True}


class UserResponse(UserBase): 
  id: int
  model_config = {"from_attributes": True}
  
   
class UserLogin(BaseModel): 
  email: EmailStr
  password: str
  
