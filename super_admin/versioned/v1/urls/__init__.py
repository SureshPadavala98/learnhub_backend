from django.urls import path,include

urlpatterns = [
    path('',include('super_admin.versioned.v1.urls.blog_urls')),
    path('mentor/',include('super_admin.versioned.v1.urls.mentor_urls')),
    path('admin/',include('super_admin.versioned.v1.urls.admin_urls')),
    path('student/',include('super_admin.versioned.v1.urls.student_urls')),

    
]