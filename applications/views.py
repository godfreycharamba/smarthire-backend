from .models import Application
from .serializers import ApplicationSerializer , ApplicationStatusSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView ,ListAPIView, RetrieveAPIView , UpdateAPIView , DestroyAPIView
from common.views import BaseAPIView

from jobs.models import Job
from profiles.models import JobSeekerProfile


class ApplicationCreateView(BaseAPIView, CreateAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        try:
            profile = JobSeekerProfile.objects.get(
                user=request.user
            )
        except JobSeekerProfile.DoesNotExist:
            return self.error_response(
                message="Job seeker profile not found",
                status_code=404
            )

        if not profile.resume_url:
            return self.error_response(
                message="You must upload your resume before applying for jobs",
                status_code=400
            )

        job_id = request.data.get("job_id")

        try:
            job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            return self.error_response(
                message="Job not found",
                status_code=404
            )

        if Application.objects.filter(
            job=job,
            applicant=profile
        ).exists():
            return self.error_response(
                message="You have already applied for this job",
                status_code=400
            )

        application = Application.objects.create(
            job=job,
            applicant=profile
        )

        return self.success_response(
            message="Application submitted successfully",
            data=ApplicationSerializer(application).data,
            status_code=201
        )

class MyApplicationsView(BaseAPIView, ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            applicant__user=self.request.user
        ).order_by("-applied_date")

    def list(self, request, *args, **kwargs):

        applications = self.get_queryset()

        return self.success_response(
            message="Applications retrieved successfully",
            data=self.get_serializer(
                applications,
                many=True
            ).data
        )
    
class ApplicationListView(BaseAPIView, ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    queryset = Application.objects.all().order_by(
        "-applied_date"
    )

    def list(self, request, *args, **kwargs):

        return self.success_response(
            message="Applications retrieved successfully",
            data=self.get_serializer(
                self.get_queryset(),
                many=True
            ).data
        )

class ApplicationDetailView(BaseAPIView, RetrieveAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "application_id"

    queryset = Application.objects.all()

    def retrieve(self, request, *args, **kwargs):

        application = self.get_object()

        return self.success_response(
            message="Application retrieved successfully",
            data=self.get_serializer(application).data
        )
    

class JobApplicationsView(BaseAPIView, ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            job__job_id=self.kwargs["job_id"]
        ).order_by("-total_match_score")

    def list(self, request, *args, **kwargs):

        applications = self.get_queryset()

        return self.success_response(
            message="Applications retrieved successfully",
            data=self.get_serializer(
                applications,
                many=True
            ).data
        )

class ApplicationStatusUpdateView(BaseAPIView, UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated]

    STATUS_FLOW = {
        "submitted": ["under_review", "rejected"],
        "under_review": ["interview", "rejected"],
        "interview": ["shortlisted", "rejected"],
        "shortlisted": ["hired", "rejected"],
        "rejected": [],
        "hired": [],
    }

    def patch(self, request, *args, **kwargs):

        try:
            application = Application.objects.get(
                application_id=self.kwargs["application_id"]
            )
        except Application.DoesNotExist:
            return self.error_response(
                message="Application not found",
                status_code=404
            )

        new_status = request.data.get("status")

        if not new_status:
            return self.error_response(
                message="Status is required",
                status_code=400
            )

        current_status = application.status

        allowed_statuses = self.STATUS_FLOW.get(
            current_status,
            []
        )

        if new_status not in allowed_statuses:
            return self.error_response(
                message=(
                    f"Cannot move application from "
                    f"'{current_status}' to '{new_status}'"
                ),
                status_code=400
            )

        application.status = new_status
        application.save()

        return self.success_response(
            message=f"Application moved to {new_status}",
            data={
                "application_id": str(
                    application.application_id
                ),
                "status": application.status
            }
        )        


class ApplicationDeleteView(BaseAPIView, DestroyAPIView):

    permission_classes = [IsAuthenticated]

    lookup_field = "application_id"

    queryset = Application.objects.all()

    def destroy(self, request, *args, **kwargs):

        application = self.get_object()

        application.delete()

        return self.success_response(
            message="Application deleted successfully"
        )            