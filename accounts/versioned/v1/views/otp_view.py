from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models.user_model import (
    User,
    PendingRegistration,
)
from accounts.versioned.v1.serializers.otp_serializer import (
    OTPSerializer,
    VerifyOTPSerializer
)
from accounts.services.otp_service import (
    OTPService,
    EmailService,
    EmailDeliveryError
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from accounts.services.auth_service import (
    AuthService
)
from accounts.versioned.v1.serializers.auth_serializer import (
    UserSerializer,
)




class SendEmailOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        
        serializers = OTPSerializer(data=request.data)

        serializers.is_valid(
            raise_exception=True
        )

        validated_data = serializers.validated_data

        email = validated_data["email"]

        otp_type = validated_data["otp_type"]

        if otp_type == "EMAIL_VERIFICATION":
            pending_registration = validated_data["pending_registration"]
            otp = OTPService.create_pending_registration_otp(pending_registration)
            user_name = pending_registration.full_name
        else:
            user = validated_data.get("user")
            otp = OTPService.create_otp(user=user,otp_type=otp_type)
            user_name = user.full_name if user else ""

        try:
            EmailService.send_otp_email(
                email=email,
                otp=otp,
                user_name=user_name,
                otp_type=otp_type,
            )
        except EmailDeliveryError as exc:
            return CustomResponse.error(
                message="OTP could not be sent",
                errors={"email": [str(exc)]},
                status_code=status.HTTP_502_BAD_GATEWAY,
            )

        return CustomResponse.success(message="OTP sent successfully",data={"OTP":otp},status_code=status.HTTP_200_OK)
    

class VerifyOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = serializer.validated_data

        email = validated_data["email"].lower()

        otp = validated_data["otp"]

        otp_type = validated_data["otp_type"]

        if otp_type == "EMAIL_VERIFICATION":

            pending_registration = PendingRegistration.objects.filter(email=email).first()

            if not pending_registration:

                return CustomResponse.error(
                    message="Registration not found. Please register again.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            OTPService.verify_pending_registration_otp(
                pending_registration=pending_registration,
                otp=otp,
            )

            # Only now is the user actually persisted to the database
            user = AuthService.create_user_from_pending(pending_registration)

        else:

            user = User.objects.filter(email=email).first()

            if not user:

                return CustomResponse.error(
                    message="User not found",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            OTPService.verify_otp(
                user=user,
                otp=otp,
                otp_type=otp_type,
            )

        # Generate JWT
        tokens = AuthService.create_tokens(user)

        user_data = UserSerializer(user).data

        return CustomResponse.success(
            message="OTP verified successfully",
            data={
                "user": user_data,
                # "tokens": tokens,
            },
            status_code=status.HTTP_200_OK
        )