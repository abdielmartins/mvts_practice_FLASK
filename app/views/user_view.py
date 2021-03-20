from flask import Blueprint, jsonify, request, make_response
from app.services.user_service import UserService

bp_user = Blueprint("bp_user", __name__)


@bp_user.route("/signup", methods=["POST"])
def signup():
    KEYS = ("name", "email", "password", "age")
    request_data = request.get_json()

    for key in KEYS:
        if not key in request_data:
            message = f"Missing {key.upper()} parameter"
            response = make_response(
                jsonify({"message": message}),
                422,
            )
            response.headers["Content-Type"] = "application/json"
            return response

    registered_user = UserService.register_user(**request_data)

    if registered_user == None:
        response = make_response(
            jsonify({}),
            422,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    response = make_response(jsonify(registered_user), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@bp_user.route("/login", methods=["POST"])
def login():
    KEYS = ("email", "password")

    request_data = request.get_json()

    for key in KEYS:
        if not key in request_data.keys():
            message = f"Missing {key.upper()} parameter"
            response = make_response(
                jsonify({"message": message}),
                422,
            )
            response.headers["Content-Type"] = "application/json"
            return response

    auth_user = UserService.login_user(request_data["email"], request_data["password"])

    if auth_user:
        response = make_response(jsonify(auth_user), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(jsonify({"message": "Invalid credentials"}), 401)
        response.headers["Content-Type"] = "application/json"
        return response


@bp_user.route("/profile/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    KEYS = ("name", "email", "password", "age")
    request_data = request.get_json()

    if not user_id:
        response = make_response(
            jsonify({"message": "Missing 'USER_ID' parameter"}),
            422,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    to_update = {}

    for key in KEYS:
        if key in request_data.keys():
            to_update[key] = request_data[key]

    updated_user = UserService.update_user(user_id, **to_update)

    if updated_user:
        response = make_response(jsonify(updated_user), 200)
        response.headers["Content-Type"] = "application/json"
        return response


@bp_user.route("/profile/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted_character = UserService.delete_user(user_id)

    if deleted_character:
        response = make_response(jsonify(), 204)
        response.headers["Content-Type"] = "application/json"
        return response


@bp_user.route("/users", methods=["GET"])
def all_users():
    found_characters = UserService.find_all_users()

    if found_characters:
        response = make_response(jsonify(found_characters), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(jsonify([]), 200)
        response.headers["Content-Type"] = "application/json"
        return response