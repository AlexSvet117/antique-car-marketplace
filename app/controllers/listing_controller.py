from flask import Blueprint, request, jsonify
from app.services.listing_service import ListingService


listing_bp = Blueprint("listings", __name__)

@listing_bp.route("/listing", methods=["POST"])
def create_listing():

    data = request.get_json()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad Request", "message" : "Data as JSON not provided"}), 400
    if "owner_id" not in data or not data.get("owner_id"):
        return jsonify({"error": "Bad Request", "message" : "owner_id as JSON not provided"}), 400
    if "make" not in data or not data.get("make"):
        return jsonify({"error": "Bad Request", "message" : "make as JSON not provided"}), 400
    if "model" not in data or not data.get("model"):
        return jsonify({"error": "Bad Request", "message" : "model as JSON not provided"}), 400
    if "body_type" not in data or not data.get("body_type"):
        return jsonify({"error": "Bad Request", "message" : "body_type as JSON not provided"}), 400

    # TODO create now the object
    listing = ListingService.create_listing(
        owner_id=data.get("owner_id"),
        make=data.get("make"),
        model=data.get("model"),
        body_type=data.get("body_type"),
        data=data
    )
    if listing:
        return jsonify({"message": "Successfully created new listing", "listing":listing.serialize()}), 201
    else: 
        return jsonify({"message": "Something went wrong while creating listing created new listing"}), 400
    

@listing_bp.route("/listing", methods=["GET"])
def get_all_listings():
    listings = ListingService.get_all_listings()
    if listings:
        return jsonify([l.serialize() for l in listings])
    else: 
        return jsonify({"message": "Seems there is an issue"}), 404