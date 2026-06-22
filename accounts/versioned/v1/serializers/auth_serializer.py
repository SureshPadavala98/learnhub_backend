from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.models.user_model import (
    User
)
from core.utils.choice_fields import (
    UserRole
)
from  mentor.models.courses import (
    Mentor
)
class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserRole.choices)

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )
        
        return value.lower()
        
    def validate(self, attrs):
        if attrs['password']!=attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        
        validate_password(attrs["password"])

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email,password=password)

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )
        
        attrs["user"] = user

        return attrs


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'role'
        ]


class MentorRegistrationSerializer(serializers.Serializer):

    bio = serializers.CharField(required=False,allow_blank=True)
    designation = serializers.CharField(required=False,allow_blank=True)
    linkedin_url = serializers.CharField(required=False,allow_blank=True)
    website = serializers.CharField(required=False,allow_blank=True)
    years_of_experience = serializers.IntegerField(min_value=0)
    profile_image = serializers.ImageField(required=False,allow_null=True)
    expertise = serializers.CharField(max_length=200)