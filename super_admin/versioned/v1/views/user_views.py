from rest_framework.views import APIView
from django.shortcuts import get_list_or_404, get_object_or_404
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
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)
from core.utils.common_models import (
    BaseAPIView
)


class MentorListAPIView(APIView):
    permission_classes = [IsAdmin]
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
    
class MentorStatusDetailAPIVIEW(APIView):
    permission_classes = [IsAdmin]


    def get(self,request,mentor_id):
        mentor = get_object_or_404(Mentor,pk=mentor_id)
                
        serializer = MentorSerializer(mentor,context={"request":request})

        return CustomResponse.success(
            message="Mentors fetched successfully",
            data =serializer.data,
        )


    def put(self,request,mentor_id):

        mentor = get_object_or_404(Mentor,pk=mentor_id)

        serializer = MentorSerializer(mentor,partial=True,data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Mentor Status updated successfully.",
            data=serializer.data
        )



