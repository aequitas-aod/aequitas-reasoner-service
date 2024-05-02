import os

from dotenv import load_dotenv, find_dotenv

if os.environ.get("TEST") == "true":
    load_dotenv(find_dotenv(".env.test"))
else:
    load_dotenv(find_dotenv(".env"))

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
