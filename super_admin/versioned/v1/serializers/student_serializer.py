from rest_framework import serializers
from super_admin.models.student_models import (
    Testimonial,
    Placement,
    Certificate,
    CertificateTemplate,
    
)


class TestimonialSerializer(serializers.ModelSerializer):
    student_image = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial

        fields = [
            'id',
            'student_name',
            'student_image',
            'designation',
            'company_name',
            'review',
            'rating',
            'display_order',
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def get_student_image(self, obj):
        request = self.context.get('request')

        if not obj.student_image:
            return None

        if request:
            return request.build_absolute_uri(obj.student_image.url)

        return obj.student_image.url
    

    def validate_rating(self,value):

        if value<1 or value >5 :
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value
    

class PlacementSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(source="course.title",read_only=True)

    class Meta:
        model = Placement

        fields = [
            "id",
            "student_name",
            "student_photo",
            "company_name",
            "company_logo",
            "designation",
            "package",
            "course",
            "course_name",
            "placement_date",
            "testimonial",
            "is_featured",
            "display_order",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class CertificateSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(source="course.title",read_only=True)

    mentor_name = serializers.CharField(source="mentor.user.full_name",read_only=True)

    class Meta:
        model = Certificate

        fields = [
            "id",
            "certificate_id",
            "student_name",
            "student_email",
            "course",
            "course_name",
            "mentor",
            "mentor_name",
            "certificate_file",
            "issued_date",
            "grade",
            "remarks",
            "is_verified",
            "created_at",
            "updated_at",

        ]

        read_only_fields = (
            "id",
            "certificate_id",
            "created_at",
            "updated_at",
        )
    


class CertificateTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CertificateTemplate

        fields = [
            "id",
            "name",
            "background_image",
            "signature_image",
            "title",
            "sub_title",
            "description",
            "layout",
            "is_default",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):

        queryset = CertificateTemplate.objects.filter(
            name__iexact=value.strip()
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Template name already exists."
            )

        return value.strip()

    def validate_layout(self, value):

        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Layout must be a valid JSON object."
            )

        return value
