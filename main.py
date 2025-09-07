from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.container import Container
from config.database import engine, Base
from api.routers.tracking_router import create_tracking_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Initialize dependency injection container
    container = Container()
    app.state.container = container
    yield


app = FastAPI(title="Tracking Service", version="0.1.0", lifespan=lifespan)

# Add router
app.include_router(create_tracking_router())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
