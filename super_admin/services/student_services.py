from django.db import transaction

from super_admin.models.student_models import (
    CertificateTemplate,
)


class CertificateTemplateService:

    @staticmethod
    @transaction.atomic
    def create_template(validated_data):

        if validated_data.get("is_default"):

            CertificateTemplate.objects.filter(
                is_default=True
            ).update(
                is_default=False
            )

        return CertificateTemplate.objects.create(
            **validated_data
        )