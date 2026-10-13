"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from humanizer.api.routes import router

app = FastAPI(
    title="Humanizer API",
    description="Transform AI-generated text into natural-sounding prose",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}