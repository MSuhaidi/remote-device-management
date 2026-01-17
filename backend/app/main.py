from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.deps import token_guard
from app.database import init_db
from app.routers import device

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(dependencies=[Depends(token_guard)], lifespan=lifespan)

app.include_router(device.router)

@app.get("/health")
def read_health():
    return {"status": "ok"}
