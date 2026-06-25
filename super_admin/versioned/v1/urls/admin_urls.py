from django.urls import path
from super_admin.versioned.v1.views import (
    user_views
)
from super_admin.versioned.v1.views import (
    courses_view,
    dashboard_views
)

urlpatterns = [
    path('dashboard/', dashboard_views.DashboardAPIView.as_view(), name='dashboard'),
    
]