from rest_framework import serializers
from mentor.models.courses import (
    CourseCategory,
    Course,
    Mentor,
    CourseInquiry,

)


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'slug',
            'created_at',
            'updated_at',
        ]

        def validate_name(self,value):
            queryset = CourseCategory.objects.filter(
                name__iexact=value.strip()
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    "Course category already exists."
                )

            return value.strip()
        

class CourseCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory

        fields = [
            "id",
            "name",
            "slug",
            "description",
        ]


class CourseSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source="category.name",read_only=True)
    mentor_name = serializers.CharField(source="mentor.user.full_name",read_only=True)


    class Meta:
        model = Course

        fields = [
            'id',
            'title',
            "slug",

            "category",
            "category_name",

            "mentor",
            "mentor_name",

            "short_description",
            "description",

            "thumbnail",

            "duration",
            "level",
            "price",

            "is_featured",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "mentor",
            "created_at",
            "updated_at",
        ]


    def validate_category(self, value):

        if not CourseCategory.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                "Invalid category."
            )

        return value
    
    def validate_mentor(self, value):

        if not Mentor.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                "Invalid Mentor ID"
            )
        
        return value
    

class CourseEnquirySerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.title",read_only=True)

    class Meta:

        model = CourseInquiry
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'course',
            'course_name',
            'message',
            'status',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]