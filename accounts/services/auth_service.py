import random
from accounts.models.user_model import (
    User
)

class AuthService:

    @staticmethod
    def create_user(*,full_name,email,password):

        user = User.objects.create(
                full_name=full_name,
                email=email,
            )
        
        user.set_password(password)
        user.save()

        return user