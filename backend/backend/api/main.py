"""
DigitalIndia Recommendation API
Main FastAPI application entrypoint.
"""
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import recommend, health

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("CIN.API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("DigitalIndia Recommendation API starting...")
    yield
    logger.info("API shutting down.")


app = FastAPI(
    title="DigitalIndia Recommendation API",
    description="AI-powered product recommendation pipeline for Indian e-commerce",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(recommend.router, prefix="/api/v1", tags=["Recommendations"])
