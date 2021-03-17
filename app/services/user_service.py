from typing import Union
import json, csv, os.path


class UserService:
    FIELDNAMES_DEFAULT = ["id", "name", "email", "password", "age"]
    FILENAME = "users.csv"

    @staticmethod
    def id_generator() -> str:
        current_id = 1
        with open(UserService.FILENAME) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for _ in csv_reader:
                current_id += 1
            return current_id

    @staticmethod
    def register_user(name: str, email: str, password: str, age: int) -> dict:
        user_id = UserService.id_generator()

        new_user = {
            "id": user_id,
            "name": name,
            "email": email,
            "password": password,
            "age": age,
        }

        with open(UserService.FILENAME) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row["email"] == email:
                    return None

        with open(UserService.FILENAME, "a") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=UserService.FIELDNAMES_DEFAULT)
            csv_writer.writerow(new_user)

        return new_user

    @staticmethod
    def find_all_users() -> list:
        with open(UserService.FILENAME) as csv_file:
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
    def find_user_by_id(user_id: int) -> Union[dict, None]:
        print(user_id)
        with open(UserService.FILENAME) as csv_file:
            user = None
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row["id"]) == user_id:
                    user = {
                        "id": int(row["id"]),
                        "name": row["name"],
                        "email": row["email"],
                        "password": row["password"],
                        "age": int(row["age"]),
                    }
            return user

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserService.find_user_by_id(user_id)

        if not user:
            return None

        for key in user:
            if key in kwargs:
                user[key] = kwargs[key]

        UserService.delete_user(user_id)

        with open(UserService.FILENAME, "a") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=UserService.FIELDNAMES_DEFAULT)
            csv_writer.writerow(user)

        return UserService.find_user_by_id(user_id)

    @staticmethod
    def delete_user(user_id: int) -> bool:
        has_user = False
        users = []

        with open(UserService.FILENAME) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if int(row["id"]) != user_id:
                    users.append(row)
                if int(row["id"]) == user_id:
                    has_user = True

        if has_user:
            with open(UserService.FILENAME, "w") as csv_file:

                csv_write_header = csv.writer(csv_file, delimiter=",", lineterminator="\n")
                csv_write_header.writerow(UserService.FIELDNAMES_DEFAULT)

                csv_writer = csv.DictWriter(csv_file, fieldnames=UserService.FIELDNAMES_DEFAULT)
                for user in users:
                    csv_writer.writerow(user)

        return has_user
