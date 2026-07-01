from django.db import models
from core.utils.common_models import CommonModel
import re

class Testimonial(CommonModel):
    student_name = models.CharField(max_length=150)

    student_image = models.ImageField(upload_to="testimonials/",blank=True,null=True)
    designation = models.CharField(max_length=150,null=True,blank=True)
    company_name = models.CharField(max_length=150,null=True,blank=True)

    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)

    is_featured = models.BooleanField(default=False)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "testimonials"
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

        ordering = [
            "display_order",
            "-created_at"
        ]

    def __str__(self):
        return f"Review By {self.student_name} - {self.rating} rating"
    


class Placement(CommonModel):
    student_name = models.CharField(max_length=150)

    student_photo = models.ImageField(upload_to="placements/students/",blank=True,null=True,)
    company_name = models.CharField(max_length=150)

    company_logo = models.ImageField(upload_to="placements/company_logos/",blank=True,null=True,)

    designation = models.CharField(max_length=150)

    package = models.DecimalField(max_digits=6,decimal_places=2,help_text="LPA")

    course = models.ForeignKey("mentor.Course",on_delete=models.SET_NULL,null=True,blank=True,related_name="placements")

    placement_date = models.DateField()

    testimonial = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "placements"
        verbose_name = "Placement"
        verbose_name_plural = "Placements"
        ordering = [
            "display_order",
            "-placement_date"
        ]
        indexes = [
            models.Index(fields=["company_name"]),
            models.Index(fields=["placement_date"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return f"{self.student_name} - {self.company_name}"


class CertificateTemplate(CommonModel):
    name = models.CharField(max_length=150,unique=True,)

    background_image = models.ImageField(upload_to="certificate_templates/backgrounds/")

    signature_image = models.ImageField(upload_to="certificate_templates/signatures/",blank=True,null=True,)
    title = models.CharField(max_length=200,default="Certificate of Completion")
    sub_title = models.CharField(max_length=250,blank=True,)
    description = models.TextField(
        help_text="""
        Available Variables

        {{student_name}}
        {{course_name}}
        {{mentor_name}}
        {{issued_date}}
        {{certificate_id}}
        {{platform_name}}
        """
            )

    layout = models.JSONField(default=dict,help_text="""Stores coordinates, font settings and alignment.""")
    is_default = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)

    class Meta:
        db_table = "certificate_templates"
        verbose_name = "Certificate Template"
        verbose_name_plural = "Certificate Templates"
        ordering = ["-created_at",]
        indexes = [
            models.Index(fields=["is_default"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):

        if self.is_default:

            CertificateTemplate.objects.filter(
                is_default=True
            ).exclude(
                pk=self.pk
            ).update(
                is_default=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Certificate(CommonModel):
    certificate_id = models.CharField(max_length=25,unique=True,editable=False)
    template = models.ForeignKey(CertificateTemplate,on_delete=models.PROTECT,related_name="certificates",null=True,blank=True,)

    student_name = models.CharField(max_length=150)

    student_email = models.EmailField(db_index=True)

    course = models.ForeignKey("mentor.Course",on_delete=models.PROTECT,related_name="certificates")

    mentor = models.ForeignKey("mentor.Mentor",on_delete=models.PROTECT,related_name="certificates")

    certificate_file = models.FileField(upload_to="certificates/",null=True,blank=True)
    qr_code = models.ImageField(upload_to="certificates/qr_codes/",blank=True,null=True,)
    issued_date = models.DateField()

    grade = models.CharField(max_length=50,blank=True)

    remarks = models.TextField(blank=True)

    is_verified = models.BooleanField(default=True)

    class Meta:
        db_table = "certificates"

        verbose_name = "Certificate"

        verbose_name_plural = "Certificates"

        ordering = ["-issued_date"]

        indexes = [
            models.Index(fields=["certificate_id"]),
            models.Index(fields=["student_email"]),
            models.Index(fields=["issued_date"]),
        ]

    def save(self, *args, **kwargs):

        if not self.certificate_id:

            last_certificate = (
                Certificate.objects
                .order_by("-created_at")
                .first()
            )

            if last_certificate and last_certificate.certificate_id:

                match = re.search(
                    r"(\d+)$",
                    last_certificate.certificate_id
                )

                next_number = (
                    int(match.group(1)) + 1
                ) if match else 1

            else:
                next_number = 1

            self.certificate_id = (
                f"STEPUPMARK-CERT-{next_number:06d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.certificate_id