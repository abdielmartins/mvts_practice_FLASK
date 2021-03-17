from flask import Flask, jsonify, request, make_response
from app.services.user_service import UserService


__version__ = "0.1.0"


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Olá mundo"

    @app.route("/signup", methods=["POST"])
    def signup():
        KEYS = ("name", "email", "password", "age")
        request_data = request.get_json()

        for key in KEYS:
            if not key in request_data:
                message = f"Missing {key.upper()} parameter"
                response = make_response(
                    jsonify({"message": message}),
                    400,
                )
                response.headers["Content-Type"] = "application/json"
                return response

        registered_user = UserService.register_user(**request_data)

        if registered_user == None:
            response = make_response(
                jsonify({"message": "Character already exists!"}),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        response = make_response(jsonify({"message": "Character created", "data": registered_user}), 200)
        response.headers["Content-Type"] = "application/json"
        return response

    @app.route("/profile/<int:user_id>", methods=["PATCH"])
    def update_user(user_id):
        KEYS = ("name", "email", "password", "age")
        request_data = request.get_json()
        print(user_id, "teste")

        if not user_id:
            response = make_response(
                jsonify({"message": "Missing 'USER_ID' parameter"}),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        to_update = {}

        for key in KEYS:
            if key in request_data.keys():
                to_update[key] = request_data[key]

        updated_user = UserService.update_user(user_id, **to_update)
        print(updated_user)

        if updated_user:
            response = make_response(jsonify({"message": "Character updated", "data": updated_user}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(jsonify({"message": "Unknown error"}), 500)
            response.headers["Content-Type"] = "application/json"
            return response

    @app.route("/profile/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        deleted_character = UserService.delete_user(user_id)

        if deleted_character:
            response = make_response(jsonify({"message": "Character deleted", "data": deleted_character}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(jsonify({"message": "Unknown error"}), 500)
            response.headers["Content-Type"] = "application/json"
            return response

    @app.route("/users", methods=["GET"])
    def all_users():
        found_characters = UserService.find_all_users()

        if found_characters:
            response = make_response(jsonify({"message": "Characters found", "data": found_characters}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        elif found_characters == []:
            response = make_response(jsonify([]), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(jsonify({"message": "Unknown error"}), 500)
            response.headers["Content-Type"] = "application/json"
            return response

    return app
