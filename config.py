import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


print(os.getenv("DB_NAME"))