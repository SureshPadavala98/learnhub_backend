from django.urls import path
from super_admin.versioned.v1.views import (
    blog_views
)

urlpatterns = [
    # Blog Category
    path('blog-category-createlist/', blog_views.BlogCategoryCreateAPIView.as_view(), name='blog-category-create'),
    path('blog-category-detail/<uuid:id>/', blog_views.BlogCategoryDetailAPIView.as_view(), name='blog-category-detail'),

    # Blog

    path('blog-create-list/', blog_views.BlogCreateAPIView.as_view(), name='blog-create-list'),
    path('blog-detail/<uuid:blog_id>/', blog_views.BlogDetailAPIView.as_view(), name='blog-detail'),



]