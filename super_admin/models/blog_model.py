from django.db import models
from django.utils.text import slugify
from core.utils.common_models import CommonModel
from accounts.models.user_model import User


class BlogCategory(CommonModel):
    name = models.CharField(max_length=100,unique=True)

    slug = models.SlugField(unique=True,blank=True)

    description = models.TextField(blank=True)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "blog_categories"
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

        ordering = [
            "display_order",
            "name"
        ]

        indexes = [
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.name)

            slug = base_slug

            counter = 1

            while BlogCategory.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Blog(CommonModel):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300,unique=True,blank=True)
    category = models.ForeignKey(BlogCategory,on_delete=models.PROTECT,related_name="blogs")
    author = models.ForeignKey(User,on_delete=models.PROTECT,related_name="blogs")
    short_description = models.CharField(max_length=350)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blogs/",blank=True,null=True)
    tags = models.CharField(max_length=300,blank=True,help_text="Comma separated tags")
    meta_title = models.CharField(max_length=255,blank=True)
    meta_description = models.CharField(max_length=300,blank=True)
    reading_time = models.PositiveIntegerField(default=5,help_text="Minutes")
    views_count = models.PositiveIntegerField(default=0,editable=False)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = "blogs"
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = [
            "-published_at",
            "-created_at"
        ]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["published_at"]),
        ]

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Blog.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title