from django.db import models
from core.utils.common_models import CommonModel


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

