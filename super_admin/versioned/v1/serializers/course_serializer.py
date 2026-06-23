from rest_framework import serializers
from mentor.models.courses import (
    CourseCategory,
    Course
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