from rest_framework.generics import CreateAPIView , ListAPIView , RetrieveAPIView , DestroyAPIView , UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from common.views import BaseAPIView
from profiles.models import EmployerProfile
from .models import Job
from .serializers import JobSerializer


class JobCreateView(BaseAPIView, CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        try:
            employer_profile = EmployerProfile.objects.get(
                user=request.user
            )
        except EmployerProfile.DoesNotExist:
            return self.error_response(
                message="Employer profile not found",
                status_code=404
            )

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(
                message="Validation failed",
                data=serializer.errors,
                status_code=400
            )

        job = serializer.save(
            employer_profile=employer_profile
        )

        return self.success_response(
            message="Job created successfully",
            data=self.get_serializer(job).data,
            status_code=201
        )
    

class JobListView(BaseAPIView, ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    def list(self, request, *args, **kwargs):

        jobs = self.get_queryset()

        return self.success_response(
            message="Jobs retrieved successfully",
            data=self.get_serializer(
                jobs,
                many=True
            ).data
        )  


class JobRetrieveView(BaseAPIView, RetrieveAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    lookup_field = "job_id"

    def retrieve(self, request, *args, **kwargs):

        job = self.get_object()

        return self.success_response(
            message="Job retrieved successfully",
            data=self.get_serializer(job).data
        )  


class JobUpdateView(BaseAPIView, UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "job_id"

    def get_queryset(self):
        return Job.objects.filter(
            employer_profile__user=self.request.user
        )

    def update(self, request, *args, **kwargs):

        job = self.get_object()

        if job.status != "draft":
            return self.error_response(
                message="Only draft jobs can be updated",
                status_code=400
            )

        serializer = self.get_serializer(
            job,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return self.error_response(
                message="Validation failed",
                data=serializer.errors,
                status_code=400
            )

        serializer.save()

        return self.success_response(
            message="Job updated successfully",
            data=serializer.data
        ) 


class PublishJobView(BaseAPIView, GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):

        try:
            job = Job.objects.get(
                job_id=job_id,
                employer_profile__user=request.user
            )
        except Job.DoesNotExist:
            return self.error_response(
                message="Job not found",
                status_code=404
            )

        if job.status != "draft":
            return self.error_response(
                message="Only draft jobs can be published",
                status_code=400
            )

        job.status = "active"
        job.save()

        return self.success_response(
            message="Job published successfully",
            data=JobSerializer(job).data
        )


class JobDeleteView(BaseAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "job_id"

    def get_queryset(self):
        return Job.objects.filter(
            employer_profile__user=self.request.user
        )

    def destroy(self, request, *args, **kwargs):

        job = self.get_object()

        job.delete()

        return self.success_response(
            message="Job deleted successfully"
        )       

