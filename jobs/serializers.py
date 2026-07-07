from rest_framework import serializers
from .models import Job
from profiles.serializers import EmployerProfileSerializer


class JobSerializer(serializers.ModelSerializer):

    employer_profile = EmployerProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = [
            "job_id",
            "employer_profile",
            "posted_date",
            "updated_at",
        ]