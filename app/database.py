from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.cover_letter_bot

users_collection = db.users
