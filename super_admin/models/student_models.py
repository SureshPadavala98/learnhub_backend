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
    