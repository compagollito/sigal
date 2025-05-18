from config.conection import get_db
from bson.objectid import ObjectId

db = get_db()
laboratory_collection = db["laboratorys"]

class LaboratorioRepository:

    @staticmethod
    def create_laboratory(data: dict) -> str:
        result = laboratory_collection.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def find_laboratory_by_id(lab_id: str) -> dict | None:
        return laboratory_collection.find_one({"_id": ObjectId(lab_id)})

    @staticmethod
    def all_laboratory() -> list:
        return list(laboratory_collection.find())

    @staticmethod
    def update_laboratory(lab_id: str, new_data: dict) -> bool:
        result = laboratory_collection.update_one(
            {"_id": ObjectId(lab_id)},
            {"$set": new_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_laboratory(lab_id: str) -> bool:
        result = laboratory_collection.delete_one({"_id": ObjectId(lab_id)})
        return result.deleted_count > 0
