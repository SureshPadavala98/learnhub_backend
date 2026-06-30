from rest_framework import serializers
from django.utils import timezone
from super_admin.models.blog_model import (
    Blog,
    BlogCategory,
)


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "display_order",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):

        qs = BlogCategory.objects.filter(name__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Category already exists."
            )

        return value.strip()
    


class BlogSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source="category.name",read_only=True)
    author_name = serializers.CharField(source="author.full_name",read_only=True)

    class Meta:
        model = Blog

        fields = [
            "id",
            "title",
            "slug",

            "category",
            "category_name",

            "author",
            "author_name",

            "short_description",
            "content",

            "featured_image",

            "tags",

            "meta_title",
            "meta_description",

            "reading_time",

            "views_count",

            "is_featured",
            "is_published",

            "published_at",

            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "id",
            "slug",
            "author",
            "views_count",
            "published_at",
            "created_at",
            "updated_at",
        )

    def validate_title(self, value):

        qs = Blog.objects.filter(
            title__iexact=value
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Blog title already exists."
            )

        return value.strip()

    def create(self, validated_data):

        if validated_data.get("is_published"):
            validated_data["published_at"] = timezone.now()

        return super().create(validated_data)

    def update(self, instance, validated_data):

        if (
            validated_data.get("is_published")
            and not instance.published_at
        ):
            validated_data["published_at"] = timezone.now()

        return super().update(instance, validated_data)