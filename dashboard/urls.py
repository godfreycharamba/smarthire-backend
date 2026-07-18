from .views import EmployerDashboardView
from django.urls import path

urlpatterns = [
        path(
        "dashboard/employer",
        EmployerDashboardView.as_view(),
        name="employer-dashboard"
    ),
]