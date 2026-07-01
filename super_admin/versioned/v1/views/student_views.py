from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
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
)
from super_admin.versioned.v1.serializers.student_serializer import (
    TestimonialSerializer,
    PlacementSerializer,
    CertificateSerializer,
    CertificateTemplateSerializer,

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
    BaseAPIView
)
from super_admin.services.student_services import (
    CertificateTemplateService,
)
from super_admin.services.qr_service import (
    QRCodeService,
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
    



class PlacementCreateListAPIView(BaseAPIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = PlacementSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Placement Profile added successfully",
            data=serializer.data
        ) 
    
    def get(self,request):
        placements = Placement.objects.filter(is_active=True).order_by("-created_at")

        paginator, paginated_categories = self.paginate_queryset(placements,request)

        serializer = PlacementSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)
        
        return CustomResponse.success(
            message="Placements fetched successfully",
            data=paginated_response.data
        )
    

class PlacementDetailAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self,request, id):
        placement_obj = get_object_or_404(Placement,pk=id,is_active=True)

        serializer = PlacementSerializer(placement_obj,context={"request": request})
        
        return CustomResponse.success(
            message="Placement Detail fetched successfully",
            data=serializer.data
        )
    

    def put(self, request,id):
        placement_obj = get_object_or_404(Placement,pk=id,is_active=True)

        serializer = PlacementSerializer(placement_obj,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Placement Updated successfully",
            data=serializer.data
        )
    
    def delete(self,request, id):
        placement_obj = get_object_or_404(Placement,pk=id,is_active=True)

        placement_obj.delete()
        
        return CustomResponse.success(
            message="Placement deleted fetched successfully",
            data={}
        ) 
    

class CertificateCreateListAPIView(BaseAPIView):
    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = CertificateSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(
            raise_exception=True
        )

        certificate = serializer.save()

        verify_url = request.build_absolute_uri(
            reverse(
                "certificate-verify",
                kwargs={"certificate_id": certificate.certificate_id},
            )
        )

        QRCodeService.generate(certificate, verify_url)

        response = CertificateSerializer(
            certificate,
            context={"request": request}
        )

        return CustomResponse.success(
            message="Certificate added successfully.",
            data=response.data,
            status_code=201,
        ) 
    
    def get(self,request):
        certificates = Certificate.objects.filter(is_active=True).order_by("-created_at")

        paginator, paginated_categories = self.paginate_queryset(certificates,request)

        serializer = CertificateSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)
        
        return CustomResponse.success(
            message="Certificates fetched successfully",
            data=paginated_response.data
        )
    

class CertificateDetailAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self,request, id):
        certificate_obj = get_object_or_404(Certificate,pk=id,is_active=True)

        serializer = CertificateSerializer(certificate_obj,context={"request": request})
        
        return CustomResponse.success(
            message="Certificate Detail fetched successfully",
            data=serializer.data
        )
    

    def put(self, request,id):
        certificate_obj = get_object_or_404(Certificate,pk=id,is_active=True)

        serializer = CertificateSerializer(certificate_obj,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Certificate Updated successfully",
            data=serializer.data
        )
    
    def delete(self,request, id):
        certificate_obj = get_object_or_404(Certificate,pk=id,is_active=True)

        certificate_obj.delete()
        
        return CustomResponse.success(
            message="Certificate deleted fetched successfully",
            data={}
        ) 
    
class CertificateTemplateCreateAPIView(BaseAPIView):

    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = CertificateTemplateSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        template = CertificateTemplateService.create_template(
            serializer.validated_data
        )

        response = CertificateTemplateSerializer(template)

        return CustomResponse.success(
            message="Certificate template created successfully.",
            data=response.data,
            status_code=201,
        )
    

    def get(self, request):

        certificate_templates = CertificateTemplate.objects.filter(is_active=True).order_by("-created_at")

        paginator, paginated_categories = self.paginate_queryset(certificate_templates,request)

        serializer = CertificateTemplateSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)
        
        return CustomResponse.success(
            message="Certificate Templates fetched successfully",
            data=paginated_response.data
        )
    

class CertificateTemplateDetailAPIView(BaseAPIView):

    permission_classes = [IsAdmin]

    def get(self, request,template_id):
        
        certificate_template_obj = get_object_or_404(CertificateTemplate,pk=template_id,is_active=True)

        serializer = CertificateTemplateSerializer(certificate_template_obj,context={"request": request})
        
        return CustomResponse.success(
            message="Certificate Template fetched successfully",
            data=serializer.data
        )


    def put(self, request,template_id):
        certificate_template_obj = get_object_or_404(CertificateTemplate,pk=template_id,is_active=True)

        serializer = CertificateTemplateSerializer(certificate_template_obj,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Certificate Template Updated successfully",
            data=serializer.data
        )
    
    def delete(self,request, template_id):
        certificate_template_obj = get_object_or_404(CertificateTemplate,pk=template_id,is_active=True)

        certificate_template_obj.delete()
        
        return CustomResponse.success(
            message="Certificate Template deleted fetched successfully",
            data={}
        )
    

class CertificateVerifyAPIView(APIView):
    permission_classes = []

    def get(self, request, certificate_id):
        certificate = get_object_or_404(
            Certificate,
            certificate_id=certificate_id,
            is_active=True
        )

        if not certificate.certificate_file:
            return CustomResponse.error(
                message="Certificate file not available.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return redirect(certificate.certificate_file.url)