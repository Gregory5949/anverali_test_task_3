import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
HOST = os.getenv("HOST")
PASSWORD = os.getenv("PASSWORD")

POSTGRES_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DBNAME}"
