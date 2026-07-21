from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from accounts.services.auth_service import (
    AuthService,
    StudentProfileService
)
from accounts.versioned.v1.serializers.auth_serializer import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    MentorRegistrationSerializer,
    StudentProfileSerializer,
    ResetPasswordSerializer,
    RefreshTokenSerializer
)
from mentor.models.courses import (
    Mentor
)
from core.utils.common_models import (
    CommonModel,
    BaseAPIView,
)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)

class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        pending_registration = AuthService.create_pending_registration(
            full_name=serializer.validated_data['full_name'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            role=serializer.validated_data['role'],
        )

        return CustomResponse.success(
            message="Registration initiated. Please verify your email with the OTP sent to complete registration.",
            data={
                "email": pending_registration.email,
                "full_name": pending_registration.full_name,
                "role": pending_registration.role,
            },
            status_code=status.HTTP_201_CREATED
        )
    
class MentorRegisrationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MentorRegistrationSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = serializer.validated_data

        mentor = Mentor.objects.create(
            user = request.user,
            bio = validated_data.get('bio', ''),
            designation= validated_data.get('designation', ''),
            website= validated_data.get('website', ''),
            years_of_experience= validated_data.get('years_of_experience', ''),
            profile_image= validated_data.get('profile_image', ''),
            expertise= validated_data.get('expertise', ''),

        )

        return CustomResponse.success(
            message="Mentor registered successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return CustomResponse.success(
            message="Login Successful",
            data={
                "access_token": str(refresh.access_token),
                "refresh": str(refresh),
                "access_token_expiry": datetime.fromtimestamp(access_token["exp"]).isoformat(),
                "refresh_token_expiry": datetime.fromtimestamp(refresh["exp"]).isoformat(),
                "user":{
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            }
        )
    

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        token = serializer.validated_data["refresh"]

        RefreshToken(token).blacklist()

        return CustomResponse.success(
            message="Logout successful",
            data={}
        )


class RefreshTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = RefreshTokenSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        tokens = AuthService.refresh_tokens(
            serializer.validated_data["refresh"]
        )

        return CustomResponse.success(
            message="Token refreshed successfully",
            data=tokens,
            status_code=status.HTTP_200_OK
        )


class ResetPasswordAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = serializer.validated_data

        AuthService.reset_password(
            validated_data["user"],
            validated_data["new_password"],
        )

        return CustomResponse.success(
            message="Password reset successful. Please login with your new password.",
            data={},
            status_code=status.HTTP_200_OK
        )


class StudentProfileAPIView(BaseAPIView):

    permission_classes = [IsStudent]

    def get(self, request):

        profile = StudentProfileService.get_or_create_profile(
            request.user
        )

        serializer = StudentProfileSerializer(
            profile,
            context={"request": request}
        )

        return CustomResponse.success(
            message="Profile fetched successfully.",
            data=serializer.data
        )

    def put(self, request):

        profile = StudentProfileService.get_or_create_profile(
            request.user
        )

        serializer = StudentProfileSerializer(
            profile,
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Profile updated successfully.",
            data=serializer.data
        )

    def patch(self, request):

        profile = StudentProfileService.get_or_create_profile(
            request.user
        )

        serializer = StudentProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Profile updated successfully.",
            data=serializer.data
        )