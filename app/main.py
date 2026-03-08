from fastapi import FastAPI
from app.database import engine
from app.models import user_model, ticket_model, comment_model
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from app.routers import analytics_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, ticket_router, comment_router
from app.routers import user_router
from app.routers import dashboard_router
from app.routers import websocket_router



app = FastAPI(title="Support Ticket System", version="1.0")
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
user_model.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(ticket_router.router)
app.include_router(comment_router.router)
app.include_router(user_router.router)
app.include_router(analytics_router.router)
app.include_router(dashboard_router.router)
app.include_router(websocket_router.router)

@app.get("/")
def home():
    return {"message": "Support Ticket API Running"}


@app.on_event("startup")
async def startup():

    redis_client = redis.from_url(
        "redis://localhost:6379",
        encoding="utf8",
        decode_responses=True,
    )

    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
