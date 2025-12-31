from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import PG_URI

engine = create_async_engine(PG_URI, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session