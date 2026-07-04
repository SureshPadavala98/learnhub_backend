from django.db import models

from core.utils.common_models import CommonModel


class SiteConfiguration(CommonModel):
    site_name = models.CharField(max_length=150)

    tagline = models.CharField(max_length=255,blank=True)
    logo = models.ImageField(upload_to="site/logo/")
    favicon = models.ImageField(upload_to="site/favicon/",blank=True,null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20,blank=True)
    address = models.TextField()
    google_map_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20,blank=True)
    support_email = models.EmailField(blank=True)
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=255,blank=True)
    meta_title = models.CharField(max_length=255,blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)

    class Meta:
        db_table = "site_configuration"
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):

        if not self.pk:
            if SiteConfiguration.objects.exists():
                raise ValueError(
                    "Only one Site Configuration is allowed."
                )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name
    

class WhyChooseUs(CommonModel):
    title = models.CharField(max_length=100,unique=True)
    short_description = models.TextField()
    icon = models.ImageField(upload_to="why_choose_us/icons/",blank=True,null=True)
    display_order = models.PositiveIntegerField(default=1)
    button_text = models.CharField(max_length=50,blank=True)
    button_url = models.CharField(max_length=255,blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = "why_choose_us"
        verbose_name = "Why Choose Us"
        verbose_name_plural = "Why Choose Us"
        ordering = ["display_order", "-created_at"]
        indexes = [
            models.Index(fields=["display_order"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return self.title