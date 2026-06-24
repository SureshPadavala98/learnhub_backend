from rest_framework import serializers
from accounts.models.user_model import (
    User,
)
from mentor.models.courses import (
    Mentor

)

class MentorSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Mentor
        fields = [
            'id',
            'user',
            'bio',
            'designation',
            'linkedin_url',
            'website',
            'years_of_experience',
            'profile_image',
            'expertise',
            'status'
        ]

    def get_profile_image(self, obj):
        request = self.context.get('request')

        if not obj.profile_image:
            return None

        if request:
            return request.build_absolute_uri(obj.profile_image.url)

        return obj.profile_image.url


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'role'
        ]