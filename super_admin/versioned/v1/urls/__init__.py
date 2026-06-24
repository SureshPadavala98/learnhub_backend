from django.urls import path,include

urlpatterns = [
    path('mentor/',include('super_admin.versioned.v1.urls.mentor_urls')),
    
]