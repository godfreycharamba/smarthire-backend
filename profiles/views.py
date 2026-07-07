from rest_framework.generics import CreateAPIView , RetrieveAPIView , DestroyAPIView , UpdateAPIView
from rest_framework.permissions import IsAuthenticated


from common.views import BaseAPIView
from common.services.supabase import upload_file

from .models import EmployerProfile , JobSeekerProfile
from .serializers import EmployerProfileSerializer , JobSeekerProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from ai_matching.services.resume_extractor import extract_resume_text
from ai_matching.services.gemini_resume_parser import parse_resume


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
    parser_classes = [MultiPartParser , FormParser]

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

        resume_url = None
        skills = []
        education = []
        experience = []

        if resume:
            try:
                # Extract resume text
                resume_text = extract_resume_text(resume)


                #Send extracted text to Gemini
                parsed_data = parse_resume(resume_text)


                #Get structured data
                skills = parsed_data.get("skills",[])

                education = parsed_data.get("education",[])

                experience = parsed_data.get("experience",[])

                # Reset file pointer after reading
                resume.seek(0)


                # 4. Upload resume to Supabase
                resume_url = upload_file(
                    file=resume,
                    folder="resumes"
                )


            except Exception as e:
                return self.error_response(
                    message=f"Resume processing failed: {str(e)}",
                    status_code=400
                )

        profile = serializer.save(
            user=request.user,
            resume_url=resume_url,
            skills=skills,
            education=education,
            experience=experience
        )

       
        return self.success_response(
            message="Job seeker profile created successfully",
            data=self.get_serializer(profile).data,
            status_code=201
        ) 

class JobSeekerProfileMeView(BaseAPIView, RetrieveAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return JobSeekerProfile.objects.get(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()

        return self.success_response(
            message="Profile retrieved successfully",
            data=self.get_serializer(profile).data
        )
    
class JobSeekerProfileUpdateView(BaseAPIView, UpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return JobSeekerProfile.objects.get(user=self.request.user)

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

        resume_url = profile.resume_url 

        if resume:
            resume_url = upload_file(
                file=resume,
                folder="resumes"
            )

        updated_profile = serializer.save(resume_url=resume_url)

        return self.success_response(
            message="Profile updated successfully",
            data=self.get_serializer(updated_profile).data,
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
