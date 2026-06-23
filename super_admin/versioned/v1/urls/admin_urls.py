from django.urls import path
from super_admin.versioned.v1.views import (
    user_views
)
from super_admin.versioned.v1.views import (
    courses_view
)

urlpatterns = [
    path('list/',user_views.MentorListAPIView.as_view(),name='mentors-list'),

    # Course Category
    path('course-category/', courses_view.CourseCategoryAPIVIEW.as_view(), name='course-categories'),
    path('course-category-detail/<uuid:category_id>/', courses_view.CourseCategoryDetailAPIVIEW.as_view(), name='course-categories'),

]