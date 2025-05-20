from typing import Optional, List
from app.models.listing import Listing
from app.extensions import db
from sqlalchemy import select

class ListingRepository:

    @staticmethod
    def create(owner_id: int, make: str, model: str, body_type: enumerate, additional_data) -> Listing :
        listing = Listing(owner_id=owner_id, make=make, model=model, body_type=body_type)
        #set additional attributes
        for key, value in additional_data.items():
            if hasattr(listing, key):
                setattr(listing, key, value)
        db.session.add(listing)
        db.session.commit()
        return listing
    
    @staticmethod
    def get_by_id(listing_id: int) -> Optional[Listing]:
        stmt = select(Listing).where(Listing.id == listing_id)
        result = db.session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def get_by_owner_id(owner_id: int) -> List[Listing]:
        stmt = select(Listing).where(Listing.owner_id == owner_id)
        results = db.session.execute(stmt)
        return list(results.scalars().all())
    
    @staticmethod
    def get_all(limit:int = 20, offset:int = 0) -> List[Listing]:
        stmt = select(Listing).limit(limit).offset(offset)
        results = db.session.execute(stmt)
        return list(results.scalars().all())
    
    @staticmethod
    def update(listing: Listing) -> Listing:
        db.session.commit()
        return listing
    
    @staticmethod
    def delete(listing: Listing) -> bool:
        db.session.delete(listing)
        db.session.commit()
        return True