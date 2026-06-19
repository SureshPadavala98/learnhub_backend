from django.db import models
from django.utils.text import slugify
from core.utils.choice_fields import (
    UserRole,
)
from core.utils.common_models import (
    CommonModel
)
from core.utils.choice_fields import (
    CourseLevel,
    InquiryStatus
)
from accounts.models.user_model import (
    User
)

class Mentor(CommonModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="mentor")
    bio = models.TextField(blank=True,null=True)
    designation = models.CharField(max_length=150,blank=True)
    linkedin_url = models.URLField(max_length=250,blank=True)
    website = models.URLField(blank=True)
    years_of_experience = models.PositiveBigIntegerField(blank=True,null=True)
    profile_image = models.ImageField(upload_to="mentor/profiles",blank=True)
    expertise = models.CharField(max_length=200,blank=True,null=True,help_text="Python,Java,Html,SQL")

    class Meta:
        db_table = "mentors"
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mentor {self.user.full_name}"

class CourseCategory(CommonModel):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=120,unique=True,blank=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table = "course_categories"
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while CourseCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.name} - Course with Slug{self.slug}"
    

class  Course(CommonModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120,unique=True,blank=True)
    category = models.ForeignKey(CourseCategory,on_delete=models.PROTECT,related_name="courses")
    mentor = models.ForeignKey(Mentor,on_delete=models.PROTECT,related_name="courses")
    short_description = models.CharField(max_length=500,blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="courses/thumbnails/",blank=True,null=True)
    duration = models.CharField(max_length=100,help_text="Example: 8 Weeks, 40 Hours")
    level = models.CharField(max_length=20,choices=CourseLevel.choices,default=CourseLevel.BEGINNER)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table="courses"
        verbose_name ="Course"
        verbose_name_plural = "Courses"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}-Mentor {self.mentor.user.full_name}"
    

class CourseInquiry(CommonModel):
    name = models.CharField(max_length=255,)
    email = models.EmailField()
    phone = models.CharField(max_length=20,)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="inquiries",)
    message = models.TextField(blank=True,null=True,)
    status = models.CharField(max_length=20,choices=InquiryStatus.choices,default=InquiryStatus.NEW,)

    class Meta:
        db_table = "course_inquiries"
        verbose_name = "Course Inquiry"
        verbose_name_plural = "Course Inquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.course.title}"

