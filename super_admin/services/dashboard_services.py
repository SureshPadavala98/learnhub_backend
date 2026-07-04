from mentor.models.courses import (
    Course,
    CourseCategory,
    Mentor,
    CourseInquiry,
)
from core.utils.choice_fields import InquiryStatus
from super_admin.models.site_configuration_model import (
    SiteConfiguration
)

class DashboardService:

    @staticmethod

    def get_dashboard_stats():

        return {
            "total_courses" : Course.objects.count(),
            
            "total_categories": CourseCategory.objects.count(),

            "total_mentors": Mentor.objects.count(),

            "total_inquiries": CourseInquiry.objects.count(),

            "new_inquiries": CourseInquiry.objects.filter(status=InquiryStatus.NEW).count(),

            "contacted_inquiries": CourseInquiry.objects.filter(status=InquiryStatus.CONTACTED).count(),

            "enrolled_inquiries": CourseInquiry.objects.filter(status=InquiryStatus.ENROLLED).count(),

        }
    

class SiteConfigurationService:

    @staticmethod
    def create_site_configuration(validated_data):

        if SiteConfiguration.objects.exists():
            raise ValueError(
                "Site configuration already exists."
            )

        return SiteConfiguration.objects.create(
            **validated_data
        )