from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.engine import make_url

# importing sessionmaker
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL



url = make_url(DATABASE_URL)

url = url.set(
    drivername="postgresql+asyncpg",
    query={
        key: value
        for key, value in url.query.items()
        if key not in {"sslmode", "channel_binding"}
    },
)



# creating database engine
engine = create_async_engine(
    url,
    echo=True,
    connect_args={"ssl": "require"}
)


# create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)