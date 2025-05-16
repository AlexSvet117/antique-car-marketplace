from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, Enum, Text, Numeric, Float
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db

class Listing(db.Model):
    __tablename__ = "listings"
    
    id = mapped_column(Integer, primary_key=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title = mapped_column(String(255), nullable=True)
    make = mapped_column(String(255), nullable=False)
    model =mapped_column(String(255), nullable=False)
    year = mapped_column(Integer, nullable=True)
    milage = mapped_column(Integer, nullable=True)
    description = mapped_column(Text, nullable=True)
    body_type = mapped_column(Enum ('sedan','hatch', 'wagon', 'coupe', 'truck','van','suv',name='body_type_enum'), nullable=False)
    price = mapped_column(Numeric(10,2), nullable=True)
    transportation_cost = mapped_column(Numeric(10,2), nullable=False)
    condition = mapped_column(String(255), nullable=True)
    color = mapped_column(String(255), nullable=True)
    is_featured = mapped_column(Boolean, nullable=True)
    status = mapped_column(Enum ('active', 'pending', 'sold', 'inactive', name='status_enum'), nullable=False)
    inspection = mapped_column(Enum ('inspected','as is', name='inspection_enum'), nullable=False)
    address = mapped_column(String(255), nullable=True)
    city = mapped_column(String(100), nullable=True)
    country = mapped_column(String(100), nullable=True)
    state = mapped_column(String(100), nullable=True)
    zip_code = mapped_column(String(100), nullable=True)
    latitude = mapped_column(Float, nullable=True)
    longitude = mapped_column(Float, nullable=True)
    created_at = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc), 
                               onupdate=lambda:datetime.now(timezone.utc), nullable=False)
    
    owner = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="listing")

    def serialize(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "title":self.title,
            "make":self.make,
            "model":self.model,
            "year":self.year,
            "milage":self.milage,
            "description":self.description,
            "body_type":self.body_type,
            "price":self.price,
            "transportation_cost":self.transportation_cost,
            "condition":self.condition,
            "color":self.color,
            "is_featured":self.is_featured,
            "status":self.status,
            "inspection":self.inspection,
            "address":self.address,
            "city":self.city,
            "country":self.country,
            "state":self.state,
            "zip_code":self.zip_code,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "created_at":self.created_at,
            "updated_at":self.updated_at
        }



