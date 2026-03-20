from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# Import models so SQLAlchemy can register them
from app.models import user_model, ticket_model, comment_model

# Routers
from app.routers import (
    auth_router,
    ticket_router,
    comment_router,
    user_router,
    analytics_router,
    dashboard_router,
    websocket_router
)

# Cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis


# ======================
# FastAPI App
# ======================

app = FastAPI(
    title="Support Ticket System",
    version="1.0"
)


# ======================
# CORS Configuration
# ======================

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================
# Database Tables
# ======================

Base.metadata.create_all(bind=engine)


# ======================
# Routers
# ======================

app.include_router(auth_router.router)
app.include_router(ticket_router.router)
app.include_router(comment_router.router)
app.include_router(user_router.router)
app.include_router(analytics_router.router)
app.include_router(dashboard_router.router)
app.include_router(websocket_router.router)


# ======================
# Home Route
# ======================

@app.get("/")
def home():
    return {"message": "Support Ticket API Running"}


# ======================
# Redis Cache Setup
# ======================

@app.on_event("startup")
async def startup():

    try:

        redis_client = redis.from_url(
            "redis://localhost:6379",
            encoding="utf8",
            decode_responses=True,
        )

        FastAPICache.init(
            RedisBackend(redis_client),
            prefix="fastapi-cache"
        )

        print("Redis Cache Connected")

    except Exception as e:

        print("Redis connection failed:", e)