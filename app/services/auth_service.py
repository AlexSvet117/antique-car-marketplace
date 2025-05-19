from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository

class AuthService:
    
    @staticmethod
    def register(email: str, username: str, password: str) -> User:
        #implement business rules
        # a user cannot register with existing email
        # user cannot register with existing username

        if UserRepository.get_by_email(email):
            raise ValueError(f"Email '{email}' already exists. Please try one more time.")
        
        if UserRepository.get_by_username(username):
            raise ValueError(f"Username '{username}' already exists. Please try one more time.")
        
        user =  UserRepository.create_user(email, username, password)

        profile = ProfileRepository.create(user.id)
        return user