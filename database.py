import os
import redis.asyncio as redis
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

load_dotenv()

user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
sslmode = os.getenv("DB_SSLMODE")

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

DATABASE_URL = (
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
)

redis_client = redis.Redis(
    host=redis_host, 
    port=redis_port, 
    decode_responses=True
)

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": "require"} if sslmode == "require" else {},
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_redis():
    yield redis_client

