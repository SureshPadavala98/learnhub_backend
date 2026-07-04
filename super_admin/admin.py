from django.contrib import admin
from super_admin.models.site_configuration_model import (
    SiteConfiguration,
    WhyChooseUs,
)
from super_admin.models.student_models import (
    Testimonial,
    Placement,
    Certificate,
    CertificateTemplate,
    Enrollment,
)
from super_admin.models.blog_model import (
    BlogCategory,
    Blog,
)
# Register your models here.

admin.site.register(Testimonial)
admin.site.register(Placement)
admin.site.register(Certificate)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(CertificateTemplate)
admin.site.register(SiteConfiguration)
admin.site.register(WhyChooseUs)
admin.site.register(Enrollment)