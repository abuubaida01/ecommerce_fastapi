from fastapi import FastAPI
from account.routers import router as account_router
from product.routers.category import router as category_router
from product.routers.product import router as product_router
from cart.router import router as cart_router
from shipping.routers import router as shipping_router
from payment.routers import router as payment_router
from order.routers import router as order_router

app = FastAPI(title="this is sample project")

app.include_router(account_router, prefix='/api/account', tags=["Account"])
app.include_router(category_router, prefix='/api/products-category', tags=['categories'])
app.include_router(product_router, prefix="/api/products", tags=['products'])
app.include_router(cart_router, prefix="/api/cart", tags=['cart'])
app.include_router(shipping_router, prefix="/api/shipping", tags=['shipping'])
app.include_router(order_router, prefix="/api/order", tags=['order'])
app.include_router(payment_router, prefix="/api/payment", tags=['payment'])
