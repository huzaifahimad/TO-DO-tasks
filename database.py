from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = getenv("MONGODB_URL", "mongodb+srv://huzaifahimadksa_db_user:abc12345@myproject1.fznryqk.mongodb.net/")
DATABASE_NAME = getenv("DATABASE_NAME", "todo_db")
COLLECTION_NAME = getenv("COLLECTION_NAME", "tasks")

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]
tasks_collection = db[COLLECTION_NAME]

def get_database():
    return db

def get_tasks_collection():
    return tasks_collection
