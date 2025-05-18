from config.conection import get_db
from bson.objectid import ObjectId

db = get_db()
user_collection = db["users"]


class UserRepository:

    @staticmethod
    def create_user(data: dict) -> str:
        result = user_collection.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def find_user_by_id(user_id: str) -> dict | None:
        return user_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def all_users() -> list:
        return list(user_collection.find())

    @staticmethod
    def update_user(user_id: str, new_data: dict) -> bool:
        result = user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": new_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_user(user_id: str) -> bool:
        result = user_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
