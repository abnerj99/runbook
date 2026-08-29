import os
from dotenv import load_dotenv


load_dotenv()

class Config:

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    #FRONTEND_URL: str = os.getenv("FRONTEND_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Config()