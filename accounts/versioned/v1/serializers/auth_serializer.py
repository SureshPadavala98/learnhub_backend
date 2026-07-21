from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.models.user_model import (
    User,
    Profile,

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
    role = serializers.CharField(required=True)

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        role = attrs.get("role")

        user = authenticate(username=email,password=password)

        if not user:
            raise serializers.ValidationError({
                "credientials": "Invalid email or password."
            })
        
        if user.role != role:
            raise serializers.ValidationError({
                "credientials": "Invalid email or password."
            })
        
        if not user.is_active:
            raise serializers.ValidationError(
                "User account is inactive."
            )

        if not user.is_email_verified:
            raise serializers.ValidationError(
                "Please verify your email before logging in."
            )

        attrs["user"] = user

        return attrs


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):

    refresh = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        email = value.lower()

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User does not exist with this email."
            )

        return email

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        validate_password(attrs['new_password'])

        attrs['user'] = User.objects.get(email=attrs['email'])

        return attrs


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



class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name",read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "user_name",
            "phone",
            "profile_picture",
            "bio",
            "city",
            "state",
            "date_of_birth",
            "gender",
            "qualification",
            "college_name",
            "graduation_year",
            "current_company",
            "experience",
            "linkedin_url",
            "github_url",
            "resume",
            "skills",
            "created_at",
            "updated_at"

        ]

        read_only_fields= [
            "id",
            "user",
            "created_at",
            "updated_at"
        ]

    def validate_phone(self, value):

        if value and not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        return value
    
    def validate_experience(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Experience cannot be negative."
            )

        return value
    