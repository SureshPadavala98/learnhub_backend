from django.urls import path,include

urlpatterns = [
    path('mentor/',include('super_admin.versioned.v1.urls.admin_urls')),
    
]