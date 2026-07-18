from rest_framework.generics import CreateAPIView , RetrieveAPIView , DestroyAPIView , UpdateAPIView
from rest_framework.permissions import IsAuthenticated
import tempfile
import os
from common.views import BaseAPIView
from common.services.supabase import upload_file
import threading
from .models import EmployerProfile , JobSeekerProfile
from .serializers import EmployerProfileSerializer , JobSeekerProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .services.resume_processing import process_resume


class EmployerProfileCreateView(BaseAPIView, CreateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if EmployerProfile.objects.filter(user=request.user).exists():
            return self.error_response(
                message="Employer profile already exists",
                status_code=400
            )

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(
                message="Validation failed",
                data=serializer.errors,
                status_code=400
            )

        profile = serializer.save(user=request.user)

        return self.success_response(
            message="Employer profile created successfully",
            data=self.get_serializer(profile).data,
            status_code=201
        )
    
class EmployerProfileRetrieveView(BaseAPIView, RetrieveAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()

        return self.success_response(
            message="Employer profile retrieved successfully",
            data=self.get_serializer(profile).data
        )   

class EmployerProfileUpdateView(BaseAPIView, UpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):

        profile = self.get_object()

        serializer = self.get_serializer(
            profile,
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
            message="Employer profile updated successfully",
            data=serializer.data
        )

class EmployerProfileDeleteView(BaseAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()

        profile.delete()

        return self.success_response(
            message="Employer profile deleted successfully"
        )  

class JobSeekerProfileCreateView(BaseAPIView, CreateAPIView):

    serializer_class = JobSeekerProfileSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]


    def create(self, request, *args, **kwargs):

        if JobSeekerProfile.objects.filter(user=request.user).exists():
            return self.error_response(
                message="Profile already exists",
                status_code=400
            )


        serializer = self.get_serializer(data=request.data)


        if not serializer.is_valid():
            return self.error_response(
                message="Validation failed",
                data=serializer.errors,
                status_code=400
            )


        resume = request.FILES.get("resume")


        # Save basic profile immediately
        profile = serializer.save(
            user=request.user,
            processing_status="pending"
        )


        if resume:
            extension = os.path.splitext(resume.name)[1]

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            )


            for chunk in resume.chunks():
                temp_file.write(chunk)


            temp_file.close()


            threading.Thread(
                target=process_resume,
                args=(
                    profile.profile_id,
                    temp_file.name
                ),
                daemon=True
            ).start()



        return self.success_response(
            message="Profile created. Resume processing started.",
            data=self.get_serializer(profile).data,
            status_code=201
        )

class JobSeekerProfileMeView(BaseAPIView, RetrieveAPIView):

    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return JobSeekerProfile.objects.get(
            user=self.request.user
        )


    def retrieve(self, request, *args, **kwargs):

        try:
            profile = self.get_object()

            return self.success_response(
                message="Profile retrieved successfully",
                data=self.get_serializer(profile).data
            )

        except JobSeekerProfile.DoesNotExist:

            return self.success_response(
                message="No profile found",
                data=[]
            )
    
class JobSeekerProfileUpdateView(BaseAPIView, UpdateAPIView):

    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def get_object(self):
        return JobSeekerProfile.objects.get(
            user=self.request.user
        )


    def update(self, request, *args, **kwargs):

        profile = self.get_object()


        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True
        )


        if not serializer.is_valid():

            return self.error_response(
                message="Validation failed",
                data=serializer.errors,
                status_code=400
            )


        resume = request.FILES.get("resume")


        # Update normal fields immediately
        updated_profile = serializer.save()


        if resume:

            updated_profile.processing_status = "pending"
            updated_profile.save()


            threading.Thread(
                target=process_resume,
                args=(
                    updated_profile.profile_id,
                    resume
                ),
                daemon=True
            ).start()



        return self.success_response(

            message=(
                "Profile updated. Resume processing started."
                if resume
                else "Profile updated successfully"
            ),

            data=self.get_serializer(
                updated_profile
            ).data,

            status_code=200
        )

class JobSeekerProfileDetailView(BaseAPIView, RetrieveAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "profile_id"

    def get_object(self):
        try:
            return JobSeekerProfile.objects.get(profile_id=self.kwargs["profile_id"])
        except JobSeekerProfile.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()

        if not profile:
            return self.error_response(
                message="Profile not found",
                status_code=404
            )

        return self.success_response(
            message="Profile retrieved successfully",
            data=self.get_serializer(profile).data
        )

class JobSeekerProfileByUserView(BaseAPIView, RetrieveAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return JobSeekerProfile.objects.get(user_id=self.kwargs["user_id"])
        except JobSeekerProfile.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()

        if not profile:
            return self.error_response(
                message="Profile not found",
                status_code=404
            )

        return self.success_response(
            message="Profile retrieved successfully",
            data=self.get_serializer(profile).data
        )            

class JobSeekerProfileDeleteView(BaseAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return JobSeekerProfile.objects.get(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.delete()

        return self.success_response(
            message="Profile deleted successfully"
            
        )                  
