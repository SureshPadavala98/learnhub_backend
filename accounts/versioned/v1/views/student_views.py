from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect,get_list_or_404
from rest_framework.permissions import AllowAny
from django.urls import reverse
from core.helpers.custom_response_hander import CustomResponse
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from super_admin.models.student_models import (
    Testimonial,
    Placement,
    Certificate,
    CertificateTemplate,
    Enrollment,
)
from super_admin.versioned.v1.serializers.student_serializer import (
    TestimonialSerializer,
    PlacementSerializer,
    CertificateSerializer,
    CertificateTemplateSerializer,
    CourseEnrollmentSerializer,

)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)
from core.utils.common_models import (
    BaseAPIView,
    PublicAPIView,

)
from super_admin.services.student_services import (
    CertificateTemplateService,
)
from super_admin.services.qr_service import (
    QRCodeService,
)
from mentor.models.courses import (
    CourseCategory,
    Course,
    Mentor,
    CourseInquiry,
)
from super_admin.versioned.v1.serializers.course_serializer import (
    CourseSerializer,
) 

class TestimoniaListAPIView(PublicAPIView):
    permission_classes = [AllowAny]

    def get(self, request):

        testimonials = Testimonial.objects.filter(is_active=True).order_by("-created_at")

        paginator, paginated_mentors = self.paginate_queryset(testimonials,request)
        serializer = TestimonialSerializer(paginated_mentors,many=True,context={"request":request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Testimonials fetched successfully",
            data =paginated_response.data,
        )

class CoursesListAPIView(PublicAPIView):
    
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
    permission_classes = [AllowAny]

    def get(self,request,course_id):

        course = get_object_or_404(Course,pk=course_id,is_active=True)

        serializer = CourseSerializer(course,context={"request":request})

        return CustomResponse.success(
            message="Course Detail fetched successfully",
            data=serializer.data
        )
    
class StudentsPlacementsListAPIView(PublicAPIView):

    def get(self,request):
        placements = Placement.objects.filter(is_active=True).order_by("-created_at")

        paginator, paginated_categories = self.paginate_queryset(placements,request)

        serializer = PlacementSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)
        
        return CustomResponse.success(
            message="Placements fetched successfully",
            data=paginated_response.data
        )
    
class StudentsPlacementDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request, id):
        placement_obj = get_object_or_404(Placement,pk=id,is_active=True)

        serializer = PlacementSerializer(placement_obj,context={"request": request})
        
        return CustomResponse.success(
            message="Placement Detail fetched successfully",
            data=serializer.data
        )
    

class StudentscertificatesAPIView(PublicAPIView):

    def get(self,request):
        certificates = Certificate.objects.filter(is_active=True).order_by("-created_at")

        paginator, paginated_categories = self.paginate_queryset(certificates,request)

        serializer = CertificateSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)
        
        return CustomResponse.success(
            message="Certificates fetched successfully",
            data=paginated_response.data
        )
    

class StudentcertificateDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self,request, id):
        certificate_obj = get_object_or_404(Certificate,pk=id,is_active=True)

        serializer = CertificateSerializer(certificate_obj,context={"request": request})
        
        return CustomResponse.success(
            message="Certificate Detail fetched successfully",
            data=serializer.data
        )