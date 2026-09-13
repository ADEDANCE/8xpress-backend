import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

# if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
#     DATABASE_URL = DATABASE_URL.replace(
#         "postgresql://",
#         "postgresql+asyncpg://",
#         1
#     )