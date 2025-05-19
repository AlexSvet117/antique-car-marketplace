from flask import Blueprint, request, jsonify
from app.utils.validators import is_valid_email, is_valid_password, is_valid_username
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    register new user
    {
	"email":"new_emai@email.com",
	"username": "new_username",
	"password": "qwerty"
    }
    Returns: 201, user successfully created
    Returns: 400, validation error
    """
    data = request.get_json()
    # validations
    if "email" not in data or not data.get("email"):
        return jsonify({"error": "Email is required"}), 400
    
    if not is_valid_email(data.get("email")):
        return jsonify({"error": f"Invalid email format {data.get("email")}"}), 400
    
    if "username" not in data or not data.get("username"):
        return jsonify({"error": "username is required"}), 400
    
    if not is_valid_username(data.get("username")):
        return jsonify({"error": f"Invalid username format, cannot contain spaces '{data.get("username")}'"}), 400
    
    if "password" not in data or not data.get("password"):
        return jsonify({"error": "password is required"}), 400
    
    if not is_valid_password(data.get("password")):
        return jsonify({"error": f"Invalid password format {data.get("password")}"}), 400
    

    try:
        user = AuthService.register(**data)
        return jsonify(
            {
                "message": "User successfully created!", 
                "user": user.serialize()
                }
            )
    except ValueError as e:
        return jsonify({"error": "Registration failed", "message": str(e)}), 400




  