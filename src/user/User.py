from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UserValidator(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    middle_name: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(..., min_length=1)
    authorized_labs: List[ObjectId] = []
    status: str
    registration_date: Optional[datetime] = None
    model_config = {"arbitrary_types_allowed": True}


class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        role: str,
        status: str,
        middle_name: Optional[str] = None,
        authorized_labs: List[ObjectId] = [],
        registration_date: Optional[datetime] = None,
        _id: Optional[ObjectId] = None,
    ):
        validated_data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "email": email,
            "password": password,
            "role": role,
            "authorized_labs": authorized_labs,
            "status": status,
            "registration_date": registration_date,
        }

        validated = UserValidator(**validated_data)

        self.__id = _id if _id is not None else ObjectId()
        self.__first_name = validated.first_name
        self.__last_name = validated.last_name
        self.__middle_name = validated.middle_name
        self.__email = validated.email
        self.__password = validated.password
        self.__role = validated.role
        self.__authorized_labs = validated.authorized_labs
        self.__status = validated.status
        self.__registration_date = (
            validated.registration_date
            if validated.registration_date is not None
            else datetime.utcnow()
        )

    # Getters
    def get_id(self) -> Optional[ObjectId]:
        return self.__id

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def get_middle_name(self) -> str:
        return self.__middle_name

    def get_email(self) -> str:
        return self.__email

    def get_password(self) -> str:
        return self.__password

    def get_role(self) -> str:
        return self.__role

    def get_authorized_labs(self) -> List[ObjectId]:
        return self.__authorized_labs

    def get_status(self) -> str:
        return self.__status

    def get_registration_date(self) -> datetime:
        return self.__registration_date

    def to_dict(self) -> dict:
        return {
            "_id": self.__id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "middle_name": self.__middle_name,
            "email": self.__email,
            "password": self.__password,
            "role": self.__role,
            "authorized_labs": self.__authorized_labs,
            "status": self.__status,
            "registration_date": self.__registration_date,
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        auth_labs_from_db = data.get("authorized_labs", [])
        status_raw = data.get("status", "Activo")

        if isinstance(status_raw, bool):
            status = "Activo" if status_raw else "Inactivo"
        elif isinstance(status_raw, str):
            status = status_raw
        else:
            status = "Activo"
        return User(
            _id=data.get("_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            middle_name=data.get("middle_name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            authorized_labs=auth_labs_from_db,
            status=status,
            registration_date=data.get("registration_date"),
        )
