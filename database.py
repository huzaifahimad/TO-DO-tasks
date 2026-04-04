from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
import sys

load_dotenv()

MONGODB_URL = getenv("MONGODB_URL")
if not MONGODB_URL:
    print("ERROR: MONGODB_URL environment variable not set!", file=sys.stderr)
    raise ValueError("MONGODB_URL is required")

DATABASE_NAME = getenv("DATABASE_NAME", "todo_db")
COLLECTION_NAME = getenv("COLLECTION_NAME", "tasks")

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
tasks_collection = db[COLLECTION_NAME]

def get_database():
    return db

def get_tasks_collection():
    return tasks_collection
