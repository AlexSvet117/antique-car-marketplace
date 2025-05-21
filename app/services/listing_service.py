from app.repositories.listing_repository import ListingRepository
from app.models.listing import Listing
from app.models.listing_image import ListingImage
from app.repositories.listing_image_repository import ListingImageRepository
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
    
    @staticmethod
    def get_listing_by_id(listing_id: int) -> Optional[Listing]:
        return ListingRepository.get_by_id(listing_id)
    
    @staticmethod
    def get_listing_by_owner(owner_id: int) -> List[Listing]:
        return ListingRepository.get_by_owner_id(owner_id)
    
    @staticmethod
    def update_listing_by_id(listing_id: int, **kwards) -> Listing:
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with id {listing_id} not found.")
        for key, value in kwards.items():
            if hasattr(listing, key):
                setattr(listing, key, value)
        return ListingRepository.update(listing)    

    @staticmethod
    def delete_listing_by_id(listing_id: int) -> bool:
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with id {listing_id} not found.")
        
        return ListingRepository.delete(listing)
    
    @staticmethod
    def add_listing_image(listing_id: int, image_url: str, cloudinary_public_id: str, 
                          is_primary: bool, caption: str) -> Optional[ListingImage]:

        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with id {listing_id} not found ")
        image = ListingImageRepository.create(
            listing_id=listing_id,
            image_url=image_url,
            claudinary_public_id=cloudinary_public_id,
            is_primary=is_primary,
            caption=caption
        )
        return image