import random
import datetime
from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from accounts.models.user_model import VerificationOTP

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

    _OTP_CONFIGS = {
        "EMAIL_VERIFICATION": {
            "subject": "Verify Your Email Address",
            "heading": "Verify your email address",
            "sub_heading": "thanks for joining LearnHub! Please use the code below to verify your email address and activate your account.",
            "body_text": "Enter this one-time password in the app to complete your email verification. Once verified, you'll have full access to all LearnHub courses and features.",
            "preheader_text": "Your LearnHub email verification code is waiting for you.",
        },
        "PASSWORD_RESET": {
            "subject": "Reset Your Password",
            "heading": "Reset your password",
            "sub_heading": "we received a request to reset the password for your LearnHub account. Use the code below to proceed.",
            "body_text": "Enter this code in the password reset screen. If you did not request a password reset, your account is still secure — please ignore this email.",
            "preheader_text": "Reset your LearnHub password with this verification code.",
        },
        "LOGIN_OTP": {
            "subject": "Your Login Verification Code",
            "heading": "One-tap login code",
            "sub_heading": "a sign-in attempt was made to your LearnHub account. Use the code below to complete the login.",
            "body_text": "This code authorises a single login session. If you did not attempt to sign in, secure your account immediately by changing your password.",
            "preheader_text": "Your LearnHub login verification code.",
        },
    }

    _DEFAULT_CONFIG = {
        "subject": "Your LearnHub OTP Code",
        "heading": "Your one-time password",
        "sub_heading": "here is your requested one-time password for LearnHub.",
        "body_text": "Use this code to complete your request on LearnHub.",
        "preheader_text": "Your LearnHub verification code.",
    }

    @classmethod
    def send_otp_email(cls, email: str, otp: str, user_name: str = "there", otp_type: str = "EMAIL_VERIFICATION") -> int:
        config = cls._OTP_CONFIGS.get(otp_type, cls._DEFAULT_CONFIG)

        context = {
            "subject": config["subject"],
            "heading": config["heading"],
            "sub_heading": config["sub_heading"],
            "body_text": config["body_text"],
            "preheader_text": config["preheader_text"],
            "user_name": user_name or "there",
            "otp": otp,
            "expiry_minutes": OTPService.OTP_EXPIRY_MINUTES,
            "recipient_email": email,
            "support_email": getattr(settings, "SUPPORT_EMAIL", settings.DEFAULT_FROM_EMAIL),
            "current_year": datetime.date.today().year,
        }

        html_body = render_to_string("accounts/emails/otp_email.html", context)
        plain_body = (
            f"Hi {context['user_name']},\n\n"
            f"{config['sub_heading'].capitalize()}\n\n"
            f"Your one-time password: {otp}\n\n"
            f"This code expires in {OTPService.OTP_EXPIRY_MINUTES} minutes.\n\n"
            "Never share this code with anyone. LearnHub staff will never ask for your OTP.\n\n"
            f"If you did not request this, contact us at {context['support_email']}.\n\n"
            "— The LearnHub Team"
        )

        try:
            msg = EmailMultiAlternatives(
                subject=f"{config['subject']} – LearnHub",
                body=plain_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            msg.attach_alternative(html_body, "text/html")
            sent_count = msg.send(fail_silently=False)
        except Exception as exc:
            raise EmailDeliveryError(f"Email backend error: {exc}") from exc

        if sent_count != 1:
            raise EmailDeliveryError("OTP email was not accepted by the email backend.")

        return sent_count
