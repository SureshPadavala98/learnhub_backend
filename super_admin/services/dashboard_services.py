from mentor.models.courses import (
    Course,
    CourseCategory,
    Mentor,
    CourseInquiry,
)
from core.utils.choice_fields import InquiryStatus


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