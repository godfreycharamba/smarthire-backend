from rest_framework import serializers
from .models import EmployerProfile , JobSeekerProfile
from accounts.serializers import UserSerializer


class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = EmployerProfile
        fields = [
            "profile_id",
            "user",
            "company_name",
            "company_website",
            "location",
            "company_description",
            "company_logo_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "profile_id",
            "created_at",
            "updated_at",
        ]

class JobSeekerProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    resume = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = JobSeekerProfile
        fields = [
            "profile_id",
            "user",
            "profile_pic_url",
            "resume",
            "resume_url",
            "title",
            "bio",
            "skills",
            "experience",
            "education",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "profile_id",
            "skills",
            "experience",
            "education",
            "resume_url",
            "created_at",
            "updated_at",
        ]  

    def create(self, validated_data):
       
        validated_data.pop('resume', None)
        return super().create(validated_data)      