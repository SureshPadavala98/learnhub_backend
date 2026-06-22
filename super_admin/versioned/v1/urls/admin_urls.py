from django.urls import path
from super_admin.versioned.v1.views import (
    user_views
)

urlpatterns = [
    path('list/',user_views.MentorListAPIView.as_view(),name='mentors-list'),

]