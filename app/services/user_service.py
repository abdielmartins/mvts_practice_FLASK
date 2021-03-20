import json, csv
from app.models.user_model import UserModel


class UserService:
    FIELDNAMES_DEFAULT = ["id", "name", "email", "password", "age"]
    FILENAME = "users.csv"

    @staticmethod
    def register_user(name: str, email: str, password: str, age: int) -> dict:
        user_id = UserModel.id_generator()

        new_user = {"id": user_id, "name": name, "email": email, "password": password, "age": age}

        if UserModel.check_user(email):
            return None

        UserModel.register_user(new_user)

        new_user.pop("password")

        return new_user

    @staticmethod
    def login_user(email: str, password: str) -> dict:
        users = UserModel.get_all_users()

        for user in users:
            print(user)
            print(email, user["email"], email == user["email"])
            print(password, user["password"], password == user["password"])
            if user["email"] == email and user["password"] == password:
                user.pop("password")
                return user

        return None

    @staticmethod
    def find_all_users() -> list:
        users = UserModel.get_all_users()

        for user in users:
            user.pop("password")

        return users

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserModel.get_user_by_id(user_id)

        for key in user:
            if key in kwargs:
                user[key] = kwargs[key]

        UserModel.delete_user(user_id)
        UserModel.register_user(user)

        return UserModel.get_user_by_id(user_id)

    @staticmethod
    def delete_user(user_id: int) -> bool:
        return UserModel.delete_user(user_id)
