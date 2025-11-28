import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import arithmetic, trigonometry, logarithms, algebra, complex_numbers, calculus, matrices, statistics, number_systems

app = FastAPI(
    title="Scientific Calculator API",
    description="A modern, fast, and feature-rich scientific calculator API.",
    version="1.0.0",
)

# CORS (Cross-Origin Resource Sharing) - More secure configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://gemini-cli-calculator.vercel.app/").split(",")

origins = [origin.strip() for origin in allowed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(arithmetic.router)
app.include_router(trigonometry.router)
app.include_router(logarithms.router)
app.include_router(algebra.router)
app.include_router(complex_numbers.router)
app.include_router(calculus.router)
app.include_router(matrices.router)
app.include_router(statistics.router)
app.include_router(number_systems.router)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and deployment verification.
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "service": "scientific-calculator-api"
    }

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Scientific Calculator API",
        "version": "1.0.0",
        "docs": "/docs"
    }