from fastapi import FastAPI
from app.api import auth, returns

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(returns.router, prefix="/api")