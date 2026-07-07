from django.urls import path

from .views import (
    ApplicationCreateView,
    MyApplicationsView,
    ApplicationListView,
    ApplicationDetailView,
    ApplicationDeleteView,
    
    ApplicationStatusUpdateView
)

urlpatterns = [

    path("applications/create/",ApplicationCreateView.as_view()),
    path("applications/mine/",MyApplicationsView.as_view()),
    path("applications/",ApplicationListView.as_view()),
    path("applications/<uuid:application_id>/",ApplicationDetailView.as_view()),
    path("applications/<uuid:application_id>/delete/",ApplicationDeleteView.as_view()),

    path("applications/<uuid:application_id>/status/",ApplicationStatusUpdateView.as_view()
),
]