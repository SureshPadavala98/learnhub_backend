from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from core.utils.choice_fields import (
    UserRole,
    OTPType,
    ChannelType,
)
from core.utils.common_models import (
    CommonModel
)

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        if not password:
            raise ValueError("Password is required")
        
        email = self.normalize_email(email)
        
        extra_fields.setdefault("role",UserRole.STUDENT)

        user = self.model(email=email,**extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email=email,password=password,**extra_fields)

class User(AbstractUser,CommonModel):
    username = None
    full_name = models.CharField(max_length=255,blank=True,default="")
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=UserRole.choices,default=UserRole.STUDENT)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return self.email



class Profile(CommonModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    phone = models.CharField(max_length=15,blank=True)
    profile_picture = models.ImageField(upload_to="profiles/",blank=True,null=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = "profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}-Profile"
    


class VerificationOTP(CommonModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='verification_otps')
    otp_hash = models.CharField(max_length=255)
    otp_type = models.CharField(max_length=50,choices=OTPType.choices)
    channel_type = models.CharField(max_length=50,choices=ChannelType.choices,default=ChannelType.EMAIL)
    destination = models.CharField(max_length=20,null=True,blank=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempt_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'verification_otps'
        verbose_name = 'Vefification OTP'
        verbose_name_plural = 'Vefification OTPs'

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['otp_type']),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"User {self.user.full_name} - OTP TYPE  -- {self.otp_type}"