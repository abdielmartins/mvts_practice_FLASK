import csv
from typing import Union


class UserModel:
    FIELDNAMES_DEFAULT = ["id", "name", "email", "password", "age"]
    FILENAME = "users.csv"

    @staticmethod
    def id_generator() -> str:
        try:
            with open(UserModel.FILENAME) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for user in csv_reader:
                    print(user["id"])
                    current_id = int(user["id"]) + 1
                return current_id
        except:
            return 1

    @staticmethod
    def check_user(user_email: str) -> bool:
        with open(UserModel.FILENAME) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["email"] == user_email:
                    return True
            return False

    @staticmethod
    def register_user(user: dict) -> bool:
        try:
            with open(UserModel.FILENAME, "a") as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=UserModel.FIELDNAMES_DEFAULT)
                csv_writer.writerow(user)
                return True
        except:
            return False

    @staticmethod
    def get_all_users() -> list:
        with open(UserModel.FILENAME) as csv_file:
            users = []
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                users.append(
                    {
                        "id": int(row["id"]),
                        "name": row["name"],
                        "email": row["email"],
                        "password": row["password"],
                        "age": int(row["age"]),
                    }
                )

            return users

    @staticmethod
    def get_user_by_id(user_id: int) -> Union[dict, None]:
        with open(UserModel.FILENAME) as csv_file:
            user = None
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row["id"]) == user_id:
                    user = {
                        "id": int(row["id"]),
                        "name": row["name"],
                        "email": row["email"],
                        "age": int(row["age"]),
                    }
            return user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        has_user = False
        users = []

        with open(UserModel.FILENAME) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row["id"]) != user_id:
                    users.append(row)
                if int(row["id"]) == user_id:
                    has_user = True

        if has_user:
            with open(UserModel.FILENAME, "w") as csv_file:

                csv_write_header = csv.writer(csv_file, delimiter=",", lineterminator="\n")
                csv_write_header.writerow(UserModel.FIELDNAMES_DEFAULT)

                csv_writer = csv.DictWriter(csv_file, fieldnames=UserModel.FIELDNAMES_DEFAULT)
                for user in users:
                    csv_writer.writerow(user)

        return has_user