from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query
from account.models import User
from db.config import session
from product.schemas import ProductCreate, ProductOut, PaginatedProductOut, ProductUpdate
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


@router.patch("/{product_id}", response_model=ProductOut)
async def product_update_by_id(
  session: session, 
  product_id: int, 
  title: str | None = Form(None), 
  description: str | None =Form(None), 
  price: float | None  = Form(None), 
  stock_quantity: int | None  = Form(None), 
  category_ids: list[int] | None = None, 
  image_url: UploadFile | None = File(None),
  admin_user: User = Depends(require_admin)
): 
  data = ProductUpdate(
    title=title, 
    description=description,
    price=price, 
    stock_quantity=stock_quantity, 
    category_ids=category_ids
  )

  product = await update_product(session, product_id, data, image_url)
  
  if not product: 
    raise HTTPException(detail="product not found", status=status.HTTP_404_NOT_FOUND)
  
  return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_product(
  session: session, 
  product_id: int, 
  admin_user: User = Depends(require_admin)
  ):

  success = await delete_product(session, product_id)
  if not success: 
    raise HTTPException(detail="product not found", status_code=status.HTTP_400_BAD_REQUEST) 


