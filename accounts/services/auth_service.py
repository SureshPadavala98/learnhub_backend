import random
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
import random
from accounts.models.user_model import (
    User
)

class AuthService:

    @staticmethod
    def create_base_user(*,full_name,email,password,role):

        user = User.objects.create(
                full_name=full_name,
                email=email,
                role=role,
            )
        
        user.set_password(password)
        user.save()

        return user

    @staticmethod
    def create_user(validated_data):

        password = validated_data.pop("password")
        validated_data['email'] = ( validated_data['email'].lower())

        email_prefix = validated_data["email"].split("@")[0]

        random_number = random.randint(1000, 9999)

        username = f"{email_prefix}-{random_number}"
        validated_data["username"] = username


        user = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()

        return user
    
    @staticmethod
    def create_tokens(user):

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "access_token_expiry": datetime.fromtimestamp(access_token["exp"]).isoformat(),
            "refresh_token_expiry": datetime.fromtimestamp(refresh["exp"]).isoformat(),
        }
    
    @staticmethod
    def logout_user(refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()
        

    @staticmethod
    def create_tokens(user):
        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

