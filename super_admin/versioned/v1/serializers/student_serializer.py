from rest_framework import serializers
from super_admin.models.student_models import (
    Testimonial,
    Placement,
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