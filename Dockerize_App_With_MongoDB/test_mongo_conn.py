import logging
from pymongo import MongoClient, errors

MONGO_URI = "mongodb+srv://houetchenougabin:houetchenougabin@cluster0.n8d671j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "coupon_data"
COLLECTION_NAME = "coupons"

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Try to list the collections to test the connection
    collections = db.list_collection_names()
    print("Connected to the database. Collections:", collections)
    
except errors.ServerSelectionTimeoutError as err:
    print("Failed to connect to the database:", err)
finally:
    client.close()
