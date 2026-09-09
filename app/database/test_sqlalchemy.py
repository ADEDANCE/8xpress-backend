import asyncio

from sqlalchemy import text
from app.database.database import engine


async def main():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        print("Database connection successful:", result.scalar())


asyncio.run(main())
