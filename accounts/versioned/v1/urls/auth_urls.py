from django.urls import path
from accounts.versioned.v1.views import (
    auth_view,
    otp_view
)

urlpatterns = [
    path('register/', auth_view.RegisterAPIView.as_view(),name='register'),
    path('login/', auth_view.LoginAPIView.as_view(), name='login'),
    path('logout/', auth_view.LogoutAPIView.as_view(),name='logout'),

    # Reset Password
    path('reset-password/', auth_view.ResetPasswordAPIView.as_view(), name='reset-password'),

    path('mentor/register/',auth_view.MentorRegisrationAPIView.as_view(),name='mentor-register'),

    # Student Profile
    path("student/profile/",auth_view.StudentProfileAPIView.as_view(),name="student-profile",),

    # OTP'S
    path('send_otp/',otp_view.SendEmailOTPAPIView.as_view()),
    path('verify_otp/',otp_view.VerifyOTPAPIView.as_view()),
]