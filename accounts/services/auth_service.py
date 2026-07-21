import random
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from django.contrib.auth.hashers import make_password
from datetime import datetime
import random
from accounts.models.user_model import (
    User,
    Profile,
    PendingRegistration,
)

class AuthService:

    @staticmethod
    def create_pending_registration(*, full_name, email, password, role):
        email = email.lower()

        PendingRegistration.objects.filter(email=email).delete()

        pending_registration = PendingRegistration.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            role=role,
        )

        return pending_registration

    @staticmethod
    def create_user_from_pending(pending_registration):

        user = User(
            full_name=pending_registration.full_name,
            email=pending_registration.email,
            role=pending_registration.role,
            is_email_verified=True,
            is_active=True,
        )
        user.password = pending_registration.password

        user.save()

        pending_registration.delete()

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
    def refresh_tokens(refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError as exc:
            raise serializers.ValidationError(str(exc))

        access_token = refresh.access_token

        if jwt_settings.ROTATE_REFRESH_TOKENS:

            if jwt_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh),
            "access_token_expiry": datetime.fromtimestamp(access_token["exp"]).isoformat(),
            "refresh_token_expiry": datetime.fromtimestamp(refresh["exp"]).isoformat(),
        }

    @staticmethod
    def reset_password(user, new_password):
        user.set_password(new_password)
        user.save(update_fields=["password"])


    @staticmethod
    def create_tokens(user):
        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

class StudentProfileService:

    @staticmethod
    def get_or_create_profile(user):

        profile, _ = Profile.objects.get_or_create(user=user)

        return profile