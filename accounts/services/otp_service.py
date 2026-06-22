import random
from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import (
    make_password
)
from accounts.models.user_model import (
    VerificationOTP
)
from django.contrib.auth.hashers import (
    check_password
)

class EmailDeliveryError(Exception):
    pass


class OTPService:
    OTP_EXPIRY_MINUTES = 5
    MAX_OTP_ATTEMPTS = 5


    @staticmethod
    def generate_otp():
        return str(random.randint(100000,999999))
    
    @classmethod
    def create_otp(cls,user,otp_type,):
        VerificationOTP.objects.filter(user=user,otp_type=otp_type,is_used=False).update(is_used=True)

        otp = cls.generate_otp()

        otp_record = VerificationOTP.objects.create(
                                            user=user,
                                            otp_hash=make_password(otp),
                                            otp_type=otp_type,
                                            expires_at=now() + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
                                        )
        
        return otp
    

    @classmethod
    def verify_otp(cls,user,otp,otp_type,):

        otp_record = (VerificationOTP.objects.filter(user=user,otp_type=otp_type,is_used=False,).order_by("-created_at").first())

        if not otp_record:
            raise ValidationError(
                "OTP not found"
            )

        # Expiry check
        if now() > otp_record.expires_at:

            otp_record.is_used = True
            otp_record.save(update_fields=["is_used"])

            raise ValidationError(
                "OTP expired"
            )

        # Attempt limit
        if (otp_record.attempt_count >=cls.MAX_OTP_ATTEMPTS):

            otp_record.is_used = True

            otp_record.save(
                update_fields=["is_used"]
            )

            raise ValidationError(
                "Maximum OTP attempts exceeded"
            )

        # Increment attempts
        otp_record.attempt_count += 1

        otp_record.save(update_fields=["attempt_count"])

        # Verify hash
        if not check_password(otp,otp_record.otp_hash):

            raise ValidationError(
                "Invalid OTP"
            )

        # Success
        otp_record.is_used = True

        otp_record.save(
            update_fields=["is_used"]
        )

        return True
    

class EmailService:

    @staticmethod
    def send_otp_email(email,otp,):
        try:
            sent_count = send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as exc:
            raise EmailDeliveryError(f"Email backend error: {exc}") from exc

        if sent_count != 1:
            raise EmailDeliveryError("OTP email was not accepted by the email backend.")

        return sent_count
