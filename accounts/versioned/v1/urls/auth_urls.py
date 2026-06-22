from django.urls import path
from accounts.versioned.v1.views import (
    auth_view,
    otp_view
)

urlpatterns = [
    path('register/', auth_view.RegisterAPIView.as_view(),name='register'),
    path('login/', auth_view.LoginAPIView.as_view(), name='login'),
    path('logout/', auth_view.LogoutAPIView.as_view(),name='logout'),

    path('mentor/register/',auth_view.MentorRegisrationAPIView.as_view(),name='mentor-register'),

    # OTP'S
    path('send_otp/',otp_view.SendEmailOTPAPIView.as_view()),
    path('verify_otp/',otp_view.VerifyOTPAPIView.as_view()),
]