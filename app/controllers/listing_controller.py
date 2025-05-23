from flask import Blueprint, request, jsonify
from app.services.listing_service import ListingService
import cloudinary.uploader
from flask_jwt_extended import jwt_required, get_jwt_identity

listing_bp = Blueprint("listings", __name__)

@listing_bp.route("/listings", methods=["POST"])
@jwt_required()
def create_listing():

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
    

@listing_bp.route("/listings", methods=["GET"])
def get_all_listings():
    listings = ListingService.get_all_listings()
    if listings:
        return jsonify([l.serialize() for l in listings])
    else: 
        return jsonify({"message": "Seems there is an issue"}), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["GET"])
@jwt_required()
def get_listing_by_id(listing_id: int):
    listing = ListingService.get_listing_by_id(listing_id)
    if listing:
        return jsonify(listing.serialize()), 200
    else: 
        return jsonify({"error": f"Listing with id {listing_id} not found"}), 400
    

@listing_bp.route("/listings/owner/<int:owner_id>", methods=["GET"])
@jwt_required()
def get_listing_by_owner_id(owner_id: int):
    listings = ListingService.get_listing_by_owner(owner_id)
    if listings:
        return jsonify([l.serialize() for l in listings]), 200
    else: 
        return jsonify({"error": f"Listing not found for owner(user) with id {owner_id}."}), 400
    


@listing_bp.route("/listings/<int:listing_id>", methods=["PUT"])
@jwt_required()
def update_listing(listing_id: int):

    data = request.get_json()

    if not data:
        return jsonify({"error": "Bad Request", "message" : "Data as JSON not provided"}), 400
    if "owner_id" in data:
        return jsonify({"error": "Bad Request", "message" : "Not allowed to change the owner id"}), 400

    try: 
        listing = ListingService.update_listing_by_id(listing_id=listing_id, **data)
        return jsonify({"message": "Successfully created new listing", "listing":listing.serialize()}), 200
    except ValueError as e:
        return jsonify({"message" : str(e)}), 404
    

@listing_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
@jwt_required()
def delete_listing(listing_id: int):
    try:
        success = ListingService.delete_listing_by_id(listing_id)
        if success:
            return jsonify({"message": f"Listing with id {listing_id} successfully deleted"})
        else: 
            return jsonify({"error": f"Listing with id {listing_id} failed to be deleted"})
    except ValueError as e:
        return jsonify({"error": "Not Found", "message": str(e)})
    

@listing_bp.route("/listings/<int:listing_id>/images", methods=["POST"])
@jwt_required()
def update_image(listing_id: int):
    listing = ListingService.get_listing_by_id(listing_id)
    if not listing:
        return jsonify({"error": f"Listing with id {listing_id} not found."}), 404
    if not request.content_type.startswith("multipart/form-data"):
        return jsonify({"error": "Content type should be multipart/form-data"})
    
    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400
    image_file = request.files.get("image")
    is_primary = request.form.get("is_primary", "")
    caption = request.form.get("caption", "")

    upload_result = cloudinary.uploader.upload(
        image_file,
        folder = "Listing Images"
    )
    listing_image = ListingService.add_listing_image(
        listing_id=listing_id,
        image_url=upload_result.get("secure_url"),
        cloudinary_public_id=upload_result.get("public_id"),
        is_primary=True if is_primary.lower() == "true" else False,
        caption=caption
    )
    if listing_image:
        return jsonify(listing_image.serialize()), 201
    else:
        return jsonify({"error": "Could not upload the iamge due to non-existent listing"}), 404
    

@listing_bp.route("/listings/<int:listing_id>/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_image(listing_id: int, image_id: int):
    listing = ListingService.get_listing_by_id(listing_id)
    if not listing:
        return jsonify({"message": f"No such listing id: {listing_id}"}), 404
    
    image_to_delete = ListingService.get_listing_image_by_id(image_id)
    
    if not image_to_delete:
        return jsonify({"message": f"No such image id {image_id}"}), 404

    result = ListingService.delete_listing_image(image_id, listing.owner_id)
    if not result:
        return jsonify({"error": " Access denied or image not found"})

    cloudinary.uploader.destroy(image_to_delete.claudinary_public_id)
    if result:
        return jsonify({"message": f"Image with id {image_id} successfully deleted"}), 200
    else:
        return jsonify({"error": "Something went wrong"}), 400
    