from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query
from account.models import User
from db.config import session
from product.schemas import ProductCreate, ProductOut, PaginatedProductOut
from account.dependency import require_admin
from typing import Annotated
from product.services import *

router = APIRouter()

@router.post("", response_model=ProductOut)
async def product_create(
    session: session,
    title: str = Form(...),
    description: str | None = Form(None),
    price: float = Form(...), 
    stock_quantity: int =Form(...),
    category_ids: Annotated[list[int], Form()] = [],
    image: UploadFile | None = File(None), 
    admin_user: User = Depends(require_admin)
  ):

  data = ProductCreate(
    title=title,
    description=description, 
    price=price,
    stock_quantity=stock_quantity, 
    category_ids=category_ids
  )

  ouput = await create_product(session=session, data=data, image_url=image)
  return ouput


@router.get("", response_model=PaginatedProductOut)
async def list_products(
  session: session, 
  categories: list[str] | None = Query(default=None), 
  limit: int = Query(default=5, ge=1, le=100),
  page: int = Query(default=1, ge=1)
): 
  return await get_all_products(session, categories, limit, page)





@router.get("/search", response_model=PaginatedProductOut)
async def products_search(
  session: session, 
  categories: list[str] | None = Query(default=None), 
  title: str | None = Query(None),
  min_price: float | None = Query(None),
  max_price: float | None = Query(None),
  limit: int = Query(default=5, ge=1, le=100),
  page: int = Query(default=1, ge=1)
  ) -> PaginatedProductOut:
  
  return await search_product(
    session=session,
    category_name=categories, 
    title=title, 
    min_price=min_price, 
    max_price=max_price,
    limit=limit,
    page = page
  )



@router.get("/{slug}", response_model=ProductOut)
async def product_get_by_slug(session: session, slug: str): 
  product = await get_product_by_slug(session, slug)

  if not product: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

  return product 
