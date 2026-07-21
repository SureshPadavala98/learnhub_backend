from rest_framework import serializers
from accounts.models.user_model import (
    VerificationOTP,
    User,
    PendingRegistration,
)
from core.utils.choice_fields import (
    ChannelType,
    OTPType
)


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_type = serializers.ChoiceField(choices=OTPType.choices)

    def validate(self, attrs):

        email = attrs.get('email').lower()
        otp_type = attrs.get('otp_type')

        if otp_type == "EMAIL_VERIFICATION":

            pending_registration = PendingRegistration.objects.filter(email=email).first()

            if not pending_registration:
                raise serializers.ValidationError({
                    "email": "No pending registration found for this email. Please register first."})

            attrs["pending_registration"] = pending_registration
            attrs["user"] = None
            return attrs

        user = User.objects.filter(email=email).first()

        if otp_type == "PASSWORD_RESET":

            if not user:
                raise serializers.ValidationError("User does not exist with this email")

        attrs["user"] = user
        return attrs
    
class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField()

    otp_type = serializers.ChoiceField(choices=OTPType.choices)