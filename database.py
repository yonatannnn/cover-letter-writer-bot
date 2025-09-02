from pymongo import MongoClient, errors
import os

MONGO_URI = os.getenv("MONGO_URI")

try:
    # Try connecting to MongoDB
    client = MongoClient(MONGO_URI)
    db = client.cover_letter_bot
    users_collection = db.users

    # Force a connection attempt
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except errors.ServerSelectionTimeoutError as e:
    print("❌ MongoDB connection failed:", e)
except errors.ConfigurationError as e:
    print("❌ Invalid MongoDB URI:", e)
except Exception as e:
    print("❌ Unexpected error while connecting to MongoDB:", e)
