from fastapi import FastAPI
from routers.auth_router import router as auth_router
from routers.prod_router import router as prod_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(prod_router)