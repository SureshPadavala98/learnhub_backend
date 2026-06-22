from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    MENTOR = "MENTOR", "Mentor"
    STUDENT = "STUDENT", "Student"


class CourseLevel(models.TextChoices):
    BEGINNER = "BEGINNER", "Beginner"
    INTERMEDIATE = "INTERMEDIATE", "Intermediate"
    ADVANCED = "ADVANCED", "Advanced"

class InquiryStatus(models.TextChoices):
    NEW = "NEW", "New"
    CONTACTED = "CONTACTED", "Contacted"
    ENROLLED = "ENROLLED", "Enrolled"
    REJECTED = "REJECTED", "Rejected"


class OTPType(models.TextChoices):
    EMAIL_VERIFICATION = 'EMAIL_VERIFICATION', 'Email Verification'
    PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset'
    LOGIN_OTP = 'LOGIN_OTP', 'Login Otp'
    PHONE_VERIFICATION  = 'PHONE_VERIFICATION', 'Phone Verification'
    

class ChannelType(models.TextChoices):
    EMAIL = 'EMAIL', 'Email'
    SMS = 'SMS', 'SMS'
    WHATSAPP = 'WHATSAPP', 'WhatsApp'

class UserStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"