from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, Enum, Text, Numeric, Float
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db

class WishlistItem(db.Model):
    __tablename__ = "wishlist_item"
    
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = mapped_column(Integer, ForeignKey("listings.id"), nullable=False)
    created_at = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc), nullable=False)

    listing = relationship("Listing", back_populates="wishlist_items")
    user = relationship("User", back_populates="wishlist_items")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "listing_id": self.listing_id,
            "created_at": self.created_at
        }
