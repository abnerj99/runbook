import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    #FRONTEND_URL: str = os.getenv("FRONTEND_URL", "")


settings = Config()