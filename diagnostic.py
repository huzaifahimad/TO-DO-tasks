import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

# Get MongoDB connection details
mongodb_url = os.getenv('MONGODB_URL')
database_name = os.getenv('DATABASE_NAME')
collection_name = os.getenv('COLLECTION_NAME')

if not mongodb_url or not database_name or not collection_name:
    print('Error: Missing environment variables')
    exit(1)

try:
    # Connect to MongoDB
    client = MongoClient(mongodb_url)
    db = client[database_name]
    collection = db[collection_name]
    
    # Test connection
    client.admin.command('ping')
    print('√ MongoDB connection successful!')
    
    # Count documents
    count = collection.count_documents({})
    print(f'√ Total documents in collection: {count}')
    
    # List all documents
    documents = list(collection.find())
    print(f'√ Found {len(documents)} documents:')
    for doc in documents:
        print(f'  - ID: {doc.get("_id")}, Title: {doc.get("title", "N/A")}, Completed: {doc.get("completed", "N/A")}')
    
except Exception as e:
    print(f'Error: {e}')