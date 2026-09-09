import asyncio

from app.database.database import test_database_connection


async def main():
    result = await test_database_connection()
    print("Database connection successful:", result)


asyncio.run(main())