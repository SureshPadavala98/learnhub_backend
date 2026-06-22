from rest_framework.views import APIView
from core.utils.choice_fields import (
    UserRole,
    UserStatus,
)
from core.helpers.custom_pagination import (
    CustomPageNumberPagination,
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from super_admin.versioned.v1.serializers.user_serializer import (
    MentorSerializer
)
from mentor.models.courses import (
    Mentor
)

class MentorListAPIView(APIView):
    permission_classes = []
    custom_pagination = CustomPageNumberPagination

    def get(self,request):
        mentors = Mentor.objects.select_related('user').filter(is_active=True).order_by('-created_at')

        paginator = self.custom_pagination()
        paginated_mentors = paginator.paginate_queryset(mentors,request)

        serializer = MentorSerializer(paginated_mentors,many=True,context={"request":request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Mentors fetched successfully",
            data =paginated_response.data,
        )