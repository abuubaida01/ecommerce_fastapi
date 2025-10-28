from fastapi import APIRouter, Depends, HTTPException, status 
from account.models import User
from db.config import session
from product import schemas as sc
from product import services as ss
from account.dependency import require_admin

router = APIRouter()

@router.post("/", response_model=sc.CategoryOut)
async def category_create(session: session, category: sc.CategoryCreate, admin_user: User = Depends(require_admin)):
  return await ss.create_category(session, category)


@router.get("/categories", response_model=list[sc.CategoryOut])
async def list_categories(session: session): 
  return await ss.list_categories(session)

 
@router.delete("/category")
async def delete_category(session: session, category_id: int, admin_user: User = Depends(require_admin)): 
  output = await ss.delete_category(session, category_id)
  if not output: 
    raise HTTPException(detail="not deleted", status_code=status.HTTP_400_BAD_REQUEST)