from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from mentor.models.courses import (
    Course,
    CourseCategory,
    Mentor,
    CourseInquiry,
)
from super_admin.services.dashboard_services import (
    DashboardService
)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)


class DashboardAPIView(APIView):

    permission_classes =  [IsAdmin]

    def get(self, request):

        data = DashboardService.get_dashboard_stats()

        return CustomResponse.success(
            message="Dashboard statistics fetched successfully.",
            data=data,
        )