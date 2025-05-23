from flask import Blueprint, request, jsonify
from app.services.listing_service import ListingService
from app.services.wishlist_item_service import WishlistItemService
import cloudinary.uploader
from flask_jwt_extended import jwt_required, get_jwt_identity

wishlist_item_bp = Blueprint("wishlist_items", __name__)

@wishlist_item_bp.route("/wishlist/<int:user_id>/listing/<int:listing_id>", methods=["POST"])
@jwt_required()
def add_wishlist_item(user_id: int, listing_id: int):
    try:
        item = WishlistItemService.add_to_wishlist(user_id=user_id, listing_id=listing_id)
        return jsonify(item.serialize())
    except ValueError as e:
        return jsonify({"error": str(e)})

@wishlist_item_bp.route("/wishlist/<int:user_id>/wishlist-item/<int:wishlist_item_id>", methods=["DELETE"])
@jwt_required()
def delete_wishlist_item(user_id: int, wishlist_item_id: int):
    item = WishlistItemService.get_item_by_id(wishlist_item_id)
    if not item:
        return jsonify({"error": f"No such item with id {wishlist_item_id}"})
    result = WishlistItemService.remove_item_from_wishlist(user_id, item.listing_id)
    if result:
        return jsonify({"message": "Item deleted successfully from wishlist"}), 200
    else:
        return jsonify({"error": "Item failed to be deleted from wishlist"}), 400
