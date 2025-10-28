from sqlalchemy.ext.asyncio import AsyncSession
from product.models import Product, Category
from product import schemas as sc
from sqlalchemy import select, func, and_
from fastapi import UploadFile, HTTPException, status
from .utils import save_upload_file, generate_slug
from slugify import slugify
from sqlalchemy.orm import selectinload

async def create_category(session: AsyncSession, category: sc.CategoryCreate) -> sc.CategoryOut: 
  category = Category(name=category.name)
  session.add(category)
  await session.commit()
  await session.refresh(category)
  return category


async def list_categories(session: AsyncSession) -> list[Category]: 
  stmt = select(Category)
  result = await session.execute(stmt)
  return result.scalars().all()


async def delete_category(session: AsyncSession, category_id: int) -> bool:
  category = await session.get(Category, category_id)
  if not category:
    return False
  await session.delete(category)
  await session.commit()
  return True


################# Products ##########33
async def create_product(session: AsyncSession, data: sc.ProductCreate, image_url: UploadFile | None = None) -> Product: 
  if data.stock_quantity < 0: 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="stock quantity can not be negative :)")
  
  image_path = await save_upload_file(image_url, "images")

  categories = []
  if data.category_ids: 
    category_stmt = select(Category).where(Category.id.in_(data.category_ids))
    category_results = await session.execute(category_stmt)
    categories = category_results.scalars().all()

  product_data_only = data.model_dump(exclude={'category_ids'})

  # generate slug, if not available
  if not product_data_only.get('slug'): 
    product_data_only['slug'] = generate_slug(product_data_only.get('title', ""))
  
  new_product = Product(**product_data_only, image_url=image_path, categories=categories)

  session.add(new_product)
  await session.commit()
  return new_product


async def get_all_products(
    session: AsyncSession, 
    category_names: list[str] | None = None, 
    limit: int = 5, 
    page: int = 1
) -> dict: 
  
  stmt  = select(Product).options(selectinload(Product.categories))

  if category_names: 
    stmt = stmt.join(Product.categories).where(Category.name.in_(category_names)).distinct()

  count_stmt = stmt.with_only_columns(func.count(Product.id)).order_by(None)
  total = await session.scalar(count_stmt) 

  stmt = stmt.limit(limit).offset((page-1)*limit)

  result = await session.execute(stmt)
  products = result.scalars().all()

  return {
    "total": total, 
    "page": page, 
    "limit": limit, 
    "items": products
  }


async def get_product_by_slug(
    session: AsyncSession, 
    slug: str
  ) -> sc.ProductOut | None: 
  
  stmt = select(Product).options(selectinload(Product.categories)).where(Product.slug == slug)
  result = await session.execute(stmt)
  return result.scalars()



async def search_product(
    session: AsyncSession,
    category_name: list[str] | None = None, 
    title: str | None = None, 
    description: str | None = None, 
    min_price: float | None = None, 
    max_price: float | None = None,  
    limit: int = 5, 
    page: int = 1
  ) -> sc.PaginatedProductOut: 
  
  stmt = select(Product).options(selectinload(Product.categories))

  if category_name: 
    stmt = stmt.join(Product.categories).where(Category.name.in_(category_name)).distinct()

  filters = []
  if title: 
    filters.append(Product.title.like(f"%{title}%"))

  if description: 
    filters.append(Product.description.like(f"%{description}%"))

  if min_price: 
    filters.append(Product.price >= min_price)
  
  if max_price: 
    filters.append(Product.price <= max_price)

  if filters: 
    stmt = stmt.where(and_(*filters))

  count_stmt = stmt.with_only_columns(func.count(Product.id)).order_by(None)
  total = await session.scalar(count_stmt) 

  stmt = stmt.limit(limit).offset((page-1)*limit)

  result = await session.execute(stmt)
  products = result.scalars().all()

  return {
    "total": total, 
    "page": page, 
    "limit": limit, 
    "items": products
  }
