from django.urls import path,include

urlpatterns = [
    path('',include('accounts.versioned.v1.urls.auth_urls')),
    
]