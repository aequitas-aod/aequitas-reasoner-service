import os

from dotenv import load_dotenv, find_dotenv

shell_env = os.environ.copy()
load_dotenv(find_dotenv('.env'), override=True)
prod_env = os.environ.copy()

ENV = shell_env.get("ENV") or prod_env.get("ENV")

if ENV == "test":
    load_dotenv(find_dotenv('.env.test'), override=True)
    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
else:
    DB_HOST = shell_env.get("DB_HOST") or prod_env.get("DB_HOST")
    DB_USER = shell_env.get("DB_USER") or prod_env.get("DB_USER")
    DB_PASSWORD = shell_env.get("DB_PASSWORD") or prod_env.get("DB_PASSWORD")
