import os

from dotenv import load_dotenv

if os.environ["TEST"] == "true":
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
