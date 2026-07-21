from django.urls import path
from accounts.versioned.v1.views import (
    auth_view,
    otp_view,
    student_views
)

urlpatterns = [

    # Testimonials
    path('testimonials-list/', student_views.TestimoniaListAPIView.as_view(),name='testimonials-list'),


    # Public End Points
    path("courses-list/", student_views.CoursesListAPIView.as_view(),name='courses-list'),
    path('course-detail/<uuid:course_id>/', student_views.CourseDetailAPIVIEW.as_view(), name='course-detail'),
    path('student-placements/',student_views.StudentsPlacementsListAPIView.as_view(),name='student-placements'),
    path('student-placement-detail/<uuid:id>/', student_views.StudentsPlacementDetailAPIView.as_view(), name='student-placement-detail'),
    path('student-certificates/',student_views.StudentscertificatesAPIView.as_view(),name='student-certificates'),
    path('student-certificate-detail/<uuid:id>/',student_views.StudentcertificateDetailAPIView.as_view(),name='student-certificates'),

]