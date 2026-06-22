from rest_framework import serializers
from accounts.models.user_model import (
    VerificationOTP,
    User
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

        user = User.objects.filter(email=email).first()

        if otp_type == "EMAIL_VERIFICATION":

            if user and user.is_email_verified :
                raise serializers.ValidationError({
                    "email":"Email already verified"})
            

        elif otp_type == "password_reset":

            if not user:
                raise serializers.ValidationError("User does not exist with this email")
            
        attrs["user"]=user
        return attrs
    
class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField()

    otp_type = serializers.ChoiceField(choices=OTPType.choices)