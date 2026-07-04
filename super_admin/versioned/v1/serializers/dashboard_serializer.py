from rest_framework import serializers

from super_admin.models.site_configuration_model import (
    SiteConfiguration,
    WhyChooseUs
)


class SiteConfigurationSerializer(serializers.ModelSerializer):

    class Meta:

        model = SiteConfiguration

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class WhyChooseUsSerializer(serializers.ModelSerializer):

    class Meta:

        model = WhyChooseUs

        fields = [
            "id",
            "title",
            "short_description",
            "icon",
            "display_order",
            "button_text",
            "button_url",
            "is_featured",
            "created_at",
            "updated_at"
        ]


        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_title(self, value):

        queryset = WhyChooseUs.objects.filter(title__iexact=value.strip())

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Title already exists."
            )

        return value.strip()
