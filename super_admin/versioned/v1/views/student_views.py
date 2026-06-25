from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from core.helpers.custom_response_hander import CustomResponse
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from super_admin.models.student_models import (
    Testimonial
)
from super_admin.versioned.v1.serializers.student_serializer import (
    TestimonialSerializer,
)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)


class TestimonialCreateListAPIView(APIView):
    permission_classes = [IsAdminOrStudent]
    custom_pagination = CustomPageNumberPagination

    def post(self, request):

        serializer = TestimonialSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Course Enquiry Created successfully.",
            data=serializer.data
        )
    

    def get(self, request):

        testimonials = Testimonial.objects.filter(is_active=True).order_by("-created_at")

        paginator = self.custom_pagination()
        paginated_mentors = paginator.paginate_queryset(testimonials,request)

        serializer = TestimonialSerializer(paginated_mentors,many=True,context={"request":request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Testimonials fetched successfully",
            data =paginated_response.data,
        )



class TestimonialDetailAPIView(APIView):
    permission_classes = [IsAdminOrStudent]

    def get(self, request,id):

        testimonial = get_object_or_404(Testimonial,is_active=True,pk=id)

        serializer = TestimonialSerializer(testimonial,context={"request":request})

        return CustomResponse.success(
            message="Testimonials fetched successfully",
            data =serializer.data, 

        )


    def put(self,request, id):

        testimonial = get_object_or_404(Testimonial,is_active=True,pk=id)

        serializer = TestimonialSerializer(testimonial,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Testimonial updated successfully",
            data =serializer.data, 

        )
    
    def delete(self, request,id):
        testimonial = Testimonial.objects.filter(is_active=True,pk=id).first()

        if not testimonial:
            return CustomResponse.error(
                message="Testimonial not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        testimonial.delete()
        
        return CustomResponse.success(
            message="Testimonial deleted successfully",
            data={}
        ) 