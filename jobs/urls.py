from django.urls import path
from .views import JobCreateView , JobListView, JobRetrieveView, JobUpdateView,JobDeleteView,PublishJobView

urlpatterns = [
    path("jobs/create/", JobCreateView.as_view()),
    path("jobs/", JobListView.as_view()),
    path("jobs/<uuid:job_id>/", JobRetrieveView.as_view()),
    path("jobs/<uuid:job_id>/update/", JobUpdateView.as_view()),
    path("jobs/<uuid:job_id>/delete/", JobDeleteView.as_view()),
    path("jobs/<uuid:job_id>/publish/", PublishJobView.as_view()),
]