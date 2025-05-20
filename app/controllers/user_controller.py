from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.utils.validators import is_valid_email, is_valid_username, is_valid_password


user_bp = Blueprint("users", __name__)

@user_bp.route("/users/<int:user_id>", methods = ["GET"])
def get_user_by_id(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if user:
        return jsonify(user.serialize()), 200
    else: 
        return jsonify({"error": "Not found","message" : f"User with id: {user_id}, not found"}), 404


@user_bp.route("/users/<int:user_id>", methods = ["PUT"])
def update_user_by_id(user_id: int):


    user = UserService.get_user_by_id(user_id)
    if not user: 
        return jsonify({"error": "Not found","message" : f"User with id: {user_id}, not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message" : "Data as JSON not provided"}), 400

    if "email" in data and (not data.get("email") or not is_valid_email(data.get("email"))):
        return jsonify({"error": "Email property fails validation"}), 400
    
    if "username" in data and (not data.get("username") or not is_valid_username(data.get("username"))):
        return jsonify({"error": "Username property fails validation"}), 400
    
    if "password" in data and (not data.get("password") or not is_valid_password(data.get("password"))):
        return jsonify({"error": "Password property fails validation"}), 400
    
    #update the record
    updated_user = UserService.update_user(user, **data)
    if updated_user:
        return jsonify({"message" : "Successfully updated", "user": updated_user.serialize()}), 200
    else:
        return jsonify({"message" : "User not updated"}), 400
    

@user_bp.route("/users/<int:user_id>/profile", methods=["GET"])
def get_user_profile(user_id: int):
    profile = UserService.get_profile_by_user_id(user_id)
    if profile:
        return jsonify(profile.serialize()), 200
    else: 
        return jsonify({"error" : "404 Not Found", "message": f"User with id {user_id} not found"}), 404
    

@user_bp.route("/users/<int:user_id>/profile", methods=["PUT"])
def update_user_profile(user_id: int):
    profile = UserService.get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error" : "404 Not Found", "message": f"Profile with id {user_id} not found"}), 404
    data = request.get_json()
    if not data: 
        return jsonify({"error" : "404 Not Found", "message": "Data as json not provided"}), 404
    # update data
    
    try: 
        profile = UserService.update_user_profile(user_id, data)
        return jsonify({"message": "User profile successfully updated",
                        "profile": profile.serialize()})
    except ValueError as e:
        return jsonify({"error": "Something went wrong", "message": str(e)})