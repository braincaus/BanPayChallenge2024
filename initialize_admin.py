from pymongo import MongoClient

from auth.jwt_handler import get_password_hash
from models.user import UserInDB

client = MongoClient("mongodb://root:example@localhost:27017")
db = client["banpay"]
users_collection = db["users"]

admin_exists = users_collection.find_one({"role": "admin"})
if not admin_exists:
    hashed_password = get_password_hash("adminpass")
    new_admin = UserInDB(
        username="admin",
        email="admin@romesistemas.mx",
        password_hash=hashed_password,
        role="admin"
    )
    users_collection.insert_one(new_admin.dict())
    print("Admin user created successfully")
else:
    print("Admin user already exists")
