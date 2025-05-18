from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_NAME = os.getenv("MONGO_NAME")

if not MONGO_URI or not MONGO_NAME:
    raise Exception("Las variables de entorno de la base de datos no está definida.")

client = MongoClient(MONGO_URI)

db = client[MONGO_NAME]


def get_db():
    return db
