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

    path("site-configuration/",dashboard_views.SiteConfigurationCreateAPIView.as_view(),name="site-configuration",),

    path("why-choose-us/",dashboard_views.WhyChooseUsCreateListAPIView.as_view(), name="why-choose-us-list-create"),
    path("why-choose-us/<uuid:why_choose_us_id>/",dashboard_views.WhyChooseUsDetailAPIView.as_view(), name="why-choose-us-list-create"),

    
]