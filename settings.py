from dotenv import load_dotenv
import os


load_dotenv(override=True)


DATABASE = {
    "dialect": os.getenv("DIALECT"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("PORT"),
    "schema": os.getenv("SCHEMA") or "public",
}


VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
