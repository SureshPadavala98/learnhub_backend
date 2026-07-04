from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from core.utils.common_models import (
    BaseAPIView
)
from super_admin.versioned.v1.serializers.dashboard_serializer import (
    SiteConfigurationSerializer,
    WhyChooseUsSerializer,
)
from mentor.models.courses import (
    Course,
    CourseCategory,
    Mentor,
    CourseInquiry,
)
from super_admin.services.dashboard_services import (
    DashboardService,
    SiteConfigurationService,
)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)
from super_admin.models.site_configuration_model import (
    SiteConfiguration,
    WhyChooseUs,

)


class DashboardAPIView(APIView):

    permission_classes =  [IsAdmin]

    def get(self, request):

        data = DashboardService.get_dashboard_stats()

        return CustomResponse.success(
            message="Dashboard statistics fetched successfully.",
            data=data,
        )
    

class SiteConfigurationCreateAPIView(BaseAPIView):

    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = SiteConfigurationSerializer(data=request.data,context={"request": request})

        serializer.is_valid(
            raise_exception=True
        )

        try:

            configuration = SiteConfigurationService.create_site_configuration(
                serializer.validated_data
            )

        except ValueError as e:

            return CustomResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        response = SiteConfigurationSerializer(
            configuration,
            context={
                "request": request
            }
        )

        return CustomResponse.success(
            message="Site configuration created successfully.",
            data=response.data,
            status_code=status.HTTP_201_CREATED
        )
    
    def get(self, request):

        site_configuration = get_object_or_404(SiteConfiguration,is_active=True)

        serializer = SiteConfigurationSerializer(site_configuration,context={"request": request})

        return CustomResponse.success(
            message="Site configuration fetched successfully.",
            data=serializer.data
        )
    

    def put(self, request):

        site_configuration = get_object_or_404(SiteConfiguration,is_active=True)

        serializer = SiteConfigurationSerializer(site_configuration,data=request.data,context={"request": request},partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return CustomResponse.success(
            message="Site configuration updated successfully.",
            data=serializer.data
        )
    


class WhyChooseUsCreateListAPIView(BaseAPIView):
    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = WhyChooseUsSerializer(data=request.data,context={"request": request})
        serializer.is_valid(
            raise_exception=True
        )

        why_choose_us = serializer.save()

        response = WhyChooseUsSerializer(why_choose_us,context={"request": request})

        return CustomResponse.success(
            message="Why Choose Us created successfully.",
            data=response.data,
            status_code=201,
        )

    def get(self, request):

        queryset = WhyChooseUs.objects.filter(is_active=True).order_by("-created_at")

        paginator, queryset = self.paginate_queryset(queryset,request)
        serializer = WhyChooseUsSerializer(queryset,many=True,context={"request": request})
        paginated_response = paginator.get_paginated_response(serializer.data)
        return CustomResponse.success(
            message="Why Choose Us fetched successfully.",
            data=paginated_response.data
        )


class WhyChooseUsDetailAPIView(BaseAPIView):

    permission_classes = [IsAdmin]

    def get(self, request, why_choose_us_id):

        why_choose_us = get_object_or_404(
            WhyChooseUs,
            pk=why_choose_us_id,
            is_active=True
        )

        serializer = WhyChooseUsSerializer(
            why_choose_us,
            context={"request": request}
        )

        return CustomResponse.success(
            message="Why Choose Us details fetched successfully.",
            data=serializer.data
        )

    def put(self, request, why_choose_us_id):

        why_choose_us = get_object_or_404(WhyChooseUs,pk=why_choose_us_id,is_active=True)
        serializer = WhyChooseUsSerializer(why_choose_us,data=request.data,context={"request": request},partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Why Choose Us updated successfully.",
            data=serializer.data
        )


    def delete(self, request, why_choose_us_id):

        why_choose_us = get_object_or_404(WhyChooseUs,pk=why_choose_us_id,is_active=True)
        why_choose_us.is_active = False
        why_choose_us.save(update_fields=["is_active"])

        return CustomResponse.success(
            message="Why Choose Us deleted successfully.",
            data={}
        )
