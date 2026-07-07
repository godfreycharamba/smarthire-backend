from django.urls import path

from .views import (
    EmployerProfileCreateView,
    EmployerProfileRetrieveView,
    EmployerProfileUpdateView,
    EmployerProfileDeleteView,

    JobSeekerProfileCreateView,
    JobSeekerProfileMeView,
   
    JobSeekerProfileDeleteView,
    JobSeekerProfileUpdateView,
    JobSeekerProfileDeleteView,
    JobSeekerProfileDetailView,
    JobSeekerProfileByUserView
)

urlpatterns = [
    path("employer-profile/create/", EmployerProfileCreateView.as_view(), name="employer-profile-create"),
    path("employer-profile/", EmployerProfileRetrieveView.as_view(), name="employer-profile-detail"),
    path("employer-profile/update/", EmployerProfileUpdateView.as_view(), name="employer-profile-update"),
    path("employer-profile/delete/", EmployerProfileDeleteView.as_view(), name="employer-profile-delete",),

     path("jobseeker-profile/create/", JobSeekerProfileCreateView.as_view()),
    path("jobseeker-profile/me/", JobSeekerProfileMeView.as_view()),
    path("jobseeker-profile/<uuid:profile_id>/", JobSeekerProfileDetailView.as_view()),
    path("jobseeker-profile/<uuid:user_id>/", JobSeekerProfileByUserView.as_view()),
    path("jobseeker-profile/update/", JobSeekerProfileUpdateView.as_view()),
    path("jobseeker-profile/delete/", JobSeekerProfileDeleteView.as_view()),
]