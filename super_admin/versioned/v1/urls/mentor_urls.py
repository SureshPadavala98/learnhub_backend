from django.urls import path
from super_admin.versioned.v1.views import (
    user_views
)
from super_admin.versioned.v1.views import (
    courses_view
)

urlpatterns = [
    path('list/',user_views.MentorListAPIView.as_view(),name='mentors-list'),
    path('detail/<uuid:mentor_id>/', user_views.MentorStatusDetailAPIVIEW.as_view(), name='mentor-detail'),

    # Course Category
    path('course-category/', courses_view.CourseCategoryAPIVIEW.as_view(), name='course-categories'),
    path('course-category-detail/<uuid:category_id>/', courses_view.CourseCategoryDetailAPIVIEW.as_view(), name='course-categories'),

    path('courses/',courses_view.CourseCreateListAPIVIEW.as_view(), name='mentor-courses'),
    path('course-detail/<uuid:course_id>/', courses_view.CourseDetailAPIVIEW.as_view(), name='course-detail'),
    path('category-courses/<uuid:category_id>/', courses_view.CourseByCategoryListAPIView.as_view(), name='category-courses'),

    # Course Inquiries
    path('course-enquiries/', courses_view.CourseEnquiryAPIVIEW.as_view(), name='course-enquiry'),
    path('course-enquiry-detail/<uuid:enquiry_id>/',courses_view.CourseEnquiryDetailAPIView.as_view(), name='course-enquiries-detail'),
    
    

]