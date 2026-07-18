from .models import Application
from jobs.models import Job
from jobs.serializers import JobSerializer
from profiles.serializers import JobSeekerProfileSerializer
from rest_framework import serializers


class ApplicationSerializer(serializers.ModelSerializer):

    job = JobSerializer(read_only=True)
    applicant = JobSeekerProfileSerializer(read_only=True)

    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(),
        source="job",
        write_only=True
    )

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = [
            "application_id",
            "applicant",
            "skills_score",
            "experience_score",
            "education_score",
            "total_match_score",
            "applied_date",
            "updated_at",
        ]

class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = [
            "status"
        ]        