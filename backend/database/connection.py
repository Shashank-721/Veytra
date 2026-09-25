#So it sets up the database connection. connects to the SQLite DB, defines AsyncSessionLocal,
# and has init_db to create the tables.
# So, no incident logic here, just the plumbing that lets the app talk to the database.
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base

DATABASE_URL = "sqlite+aiosqlite:///./veytra.db"

#engine let you converse with the database
engine = create_async_engine(DATABASE_URL)

#workspace for one session job
AsyncSessionLocal = async_sessionmaker(engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Create all database tables defined by our SQLAlchemy models
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
