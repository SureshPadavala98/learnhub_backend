from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from super_admin.versioned.v1.serializers.course_serializer import (
    CourseSerializer,
    CourseCategoryListSerializer,
)
from mentor.models.courses import (
    CourseCategory
)
from core.utils.common_models import (
    BaseAPIView
)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)


class CourseCategoryAPIVIEW(BaseAPIView):
    permission_classes = [IsAdmin]

    def post(self, request):

        serializer  = CourseSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = serializer.save()

        return CustomResponse.success(
            message="Course category created successfully.",
            data=CourseCategoryListSerializer(
                category
            ).data
        )
    
    def get(self, request):

        course_categories = CourseCategory.objects.filter(is_active=True).order_by('-created_at')

        paginator, paginated_categories = self.paginate_queryset(course_categories,request)

        serializer = CourseSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Course categories fetched successfully",
            data=paginated_response.data
        )



class  CourseCategoryDetailAPIVIEW(APIView):
    permission_classes = []

    def put(self,request, category_id):
        category = get_object_or_404(CourseCategory,pk=category_id)

        serializer = CourseSerializer(category,data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Course category updated successfully.",
            data=serializer.data
        )




    def get(self,request, category_id):

        category = get_object_or_404(CourseCategory,pk=category_id)

        serializer = CourseSerializer(category,context={"request": request})

        return CustomResponse.success(
            message="Course category fetched successfully",
            data=serializer.data
        )
    


    def delete(self, request, category_id):
        category = get_object_or_404(CourseCategory,pk=category_id)

        category.delete()

        return CustomResponse.success(
            message="Course category deleted successfully",
            data={}
        )