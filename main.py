from fastapi import FastAPI
from account.routers import router

app = FastAPI(title="this is sample project")

app.include_router(router, prefix='/api/account')