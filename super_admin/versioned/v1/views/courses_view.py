from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from super_admin.versioned.v1.serializers.course_serializer import (
    CourseSerializer,
    CourseCategoryListSerializer,
    CourseSerializer,
    CourseEnquirySerializer,
)
from mentor.models.courses import (
    CourseCategory,
    Course,
    Mentor,
    CourseInquiry,
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
    


class CourseCreateListAPIVIEW(BaseAPIView):

    permission_classes = [IsAdminOrMentor]

    def post(self,request):

        mentor = get_object_or_404(Mentor,user=request.user,is_active=True)

        serializer = CourseSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(mentor=mentor)

        return CustomResponse.success(
            message="Course Created successfully.",
            data=serializer.data
        )
    

    def get(self,request):

        courses = get_list_or_404(Course,is_active=True)

        paginator, paginated_categories = self.paginate_queryset(courses,request)

        serializer = CourseSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Courses fetched successfully",
            data=paginated_response.data
        )
    

class CourseDetailAPIVIEW(APIView):
    permission_classes = [IsAdminOrMentor]

    def get(self,request,course_id):

        course = get_object_or_404(Course,pk=course_id,is_active=True)

        serializer = CourseSerializer(course,context={"request":request})

        return CustomResponse.success(
            message="Course Detail fetched successfully",
            data=serializer.data
        )
    

    def put(self, request, course_id):

        course = get_object_or_404(Course,pk=course_id,is_active=True)

        serializer = CourseSerializer(course,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Course Detail Updated successfully",
            data=serializer.data
        )
    

    def delete(self, request, course_id):

        course = get_object_or_404(Course,pk=course_id,is_active=True)

        course.delete()

        return CustomResponse.success(
            message="Course Deleted successfully",
            data={},
        )
    

class CourseByCategoryListAPIView(BaseAPIView):
    permission_classes = []

    def get(self, request, category_id):

        courses = get_list_or_404(Course,category_id=category_id,is_active=True)

        paginator, paginated_categories = self.paginate_queryset(courses,request)

        serializer = CourseSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Courses fetched successfully",
            data=paginated_response.data
        )
    

class CourseEnquiryAPIVIEW(BaseAPIView):
    permission_classes = []

    def post(self, request):

        serializer = CourseEnquirySerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Course Enquiry Created successfully.",
            data=serializer.data
        )
    
    def get(self, request):

        course_enquiries = CourseInquiry.objects.filter(is_active=True).order_by("-created_at")

        enquiry_status = request.query_params.get("status")

        if enquiry_status:
            course_enquiries = course_enquiries.filter(status=enquiry_status)
    
        paginator, paginated_categories = self.paginate_queryset(course_enquiries,request)

        serializer = CourseEnquirySerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Course Enquiry fetched successfully",
            data=paginated_response.data
        )

class CourseEnquiryDetailAPIView(APIView):
    permission_classes =[]

    def put(self, request,enquiry_id):

        enquiry = get_object_or_404(CourseInquiry,id=enquiry_id,is_active=True)

        serializer = CourseEnquirySerializer(enquiry,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Course Enquiry Updated successfully.",
            data=serializer.data
        )
    
    def get(self, request,enquiry_id):

        courses_enquiries = get_object_or_404(CourseInquiry,id=enquiry_id,is_active=True)

        serializer = CourseEnquirySerializer(courses_enquiries,context={"request": request})

        return CustomResponse.success(
            message="Course Enquiry Detail fetched successfully",
            data=serializer.data
        )
        