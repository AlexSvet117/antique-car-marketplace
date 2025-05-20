from app.repositories.listing_repository import ListingRepository
from app.models.listing import Listing
from typing import Optional, List, Dict, Any

class ListingService:

    @staticmethod
    def create_listing(owner_id: int, make: str, model: str, body_type, data: Dict[str,Any]) -> Listing:
        extra_data = {key:value for key, value in data.items() if key not in ("owner_id", "make", "model", "body_type")}
        return ListingRepository.create(
            owner_id=owner_id, 
            make=make, 
            model=model, 
            body_type=body_type, 
            additional_data=extra_data
            )
    
    @staticmethod
    def get_all_listings() -> List[Listing]:
        return ListingRepository.get_all()