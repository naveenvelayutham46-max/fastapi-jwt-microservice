from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, items

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI JWT Authentication Microservice",
    description=(
        "Secure REST API with user registration, JWT authentication, "
        "Pydantic validation, SQLite persistence, and protected CRUD operations."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(items.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "FastAPI JWT Microservice is running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
