import os
import sys

from dotenv import load_dotenv

load_dotenv(sys.path[1] + '/.env')

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
