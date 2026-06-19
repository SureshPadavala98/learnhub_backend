from django.contrib import admin
from mentor.models.courses import (
    Mentor,
    CourseCategory,
    Course,
    CourseInquiry
)

# Register your models here.

admin.site.register(Mentor)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseInquiry)