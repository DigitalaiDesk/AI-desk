from fastapi import FastAPI

from app.api.routes import router
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Desk Intelligence")
app.include_router(router, prefix="/api/v1")
