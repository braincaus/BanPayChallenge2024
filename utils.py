import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]
users_collection = db["users"]


def get_all_users():
    return users_collection.find()


def get_user(query: dict):
    return users_collection.find_one(query)


def insert_user(user: dict):
    return users_collection.insert_one(user)
