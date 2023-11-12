from app.config.settings import settings
from pymongo.mongo_client import MongoClient
from pymongo import ASCENDING

client = MongoClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

try:
    client.server_info()
    print(f'Connected to mongodb at: {settings.DATABASE_URL}')
except Exception as e:
    print(f'Could not connected to mongodb at: {settings.DATABASE_URL}')
    print(e)

db = client.get_database(settings.MONGO_INITDB_DATABASE)
Users = db.get_collection('Users')
Users.create_index([("email", ASCENDING)], unique=True)
