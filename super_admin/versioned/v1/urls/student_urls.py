from django.urls import path
from super_admin.versioned.v1.views import (
    user_views
)
from super_admin.versioned.v1.views import (
    courses_view,
    dashboard_views,
    student_views
)

urlpatterns = [
    path('testimonials/', student_views.TestimonialCreateListAPIView.as_view(), name='testimonials'),
    path('testimonial-detail/<uuid:id>/', student_views.TestimonialDetailAPIView.as_view(), name='testimonial-detail'),

    # Placements
    path('placements/', student_views.PlacementCreateListAPIView.as_view(), name='students-placements'),
    path('placement-detail/<uuid:id>/', student_views.PlacementDetailAPIView.as_view(), name='student-placement-detail'),
    
]