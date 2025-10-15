from pydantic import BaseModel, EmailStr, Field, field_validator

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
  

class ChangePassword(BaseModel): 
  old_password: str = Field(...)
  new_password: str = Field(..., min_lenght=8)

  @field_validator("new_password")
  @classmethod
  def validate_new_password_strength(cls, value: str) -> str: 
    if value.lower() == value or value.upper() == value:
      raise ValueError("Password must contain both uppercase and lowercase letters")
    if not any(char.isdigit() for char in value):
      raise ValueError("Password must contain at least one digit")
    return value
  


class ForgetPassword(BaseModel): 
  email: EmailStr


class ResetPassword(BaseModel): 
  token: str
  new_password: str = Field(..., min_lenght=8)

  @field_validator("new_password")
  @classmethod
  def validate_new_password_strength(cls, value: str) -> str: 
    if value.lower() == value or value.upper() == value:
      raise ValueError("Password must contain both uppercase and lowercase letters")
    if not any(char.isdigit() for char in value):
      raise ValueError("Password must contain at least one digit")
    return value
  