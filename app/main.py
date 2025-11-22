from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import arithmetic, trigonometry, logarithms, algebra, complex_numbers, calculus, matrices, statistics, number_systems

app = FastAPI(
    title="Scientific Calculator API",
    description="A modern, fast, and feature-rich scientific calculator API.",
    version="1.0.0",
)

# CORS (Cross-Origin Resource Sharing)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    Health check endpoint.
    """
    return {"status": "ok"}
