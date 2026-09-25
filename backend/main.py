from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.incident_routes import router as incident_router
from .database.connection import init_db


# Runs when the FastAPI application starts and shuts down
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database before accepting requests
    await init_db()

    yield

    # Shutdown logic will go here later
    # For now, there is nothing to clean up


# Create the FastAPI application
app = FastAPI(
    title="Veytra",
    lifespan=lifespan,
)
app.include_router(incident_router) #Take all the endpoints defined inside incident_router and make them part of this application.

# Simple health-check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}