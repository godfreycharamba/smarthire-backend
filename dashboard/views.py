from common.views import BaseAPIView
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from profiles.models import EmployerProfile
from applications.models import Application
from jobs.models import Job

class EmployerDashboardView(BaseAPIView, APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            employer = EmployerProfile.objects.get(
                user=request.user
            )
        except EmployerProfile.DoesNotExist:
            return self.error_response(
                message="Employer profile not found",
                status_code=404
            )

        jobs = Job.objects.filter(
            employer_profile=employer
        )

        applications = Application.objects.filter(
            job__employer_profile=employer
        )

        total_jobs = jobs.count()

        total_applications = applications.count()

        average_match_score = (
            applications.aggregate(
                avg=Avg("total_match_score")
            )["avg"] or 0
        )

        top_candidates = applications.filter(
            total_match_score__gte=90
        ).count()

        job_chart = []

        for job in jobs:

            job_chart.append({
                "job_id": str(job.job_id),
                "job_title": job.title,
                "applications": job.applications.count()
            })

        match_distribution = {
                "90_100": 0,
                "80_89": 0,
                "70_79": 0,
                "below_70": 0
            }

        for application in applications:

            score = float(
                application.total_match_score
            )

            if score >= 90:
                match_distribution["90_100"] += 1

            elif score >= 80:
                match_distribution["80_89"] += 1

            elif score >= 70:
                match_distribution["70_79"] += 1

            else:
                match_distribution["below_70"] += 1   

        recent_jobs = jobs.order_by(
                "-posted_date"
            )[:5]

        recent_jobs_data = []

        for job in recent_jobs:

            recent_jobs_data.append({
                "job_id": str(job.job_id),
                "title": job.title,
                "location": job.location,
                "posted_date": job.posted_date,
                "applicants": job.applications.count(),
                "status": job.status
            }) 

        recent_applications = applications.order_by(
                "-applied_date"
            )[:5]

        recent_applications_data = []

        for application in recent_applications:

            recent_applications_data.append({
                "application_id": str(
                    application.application_id
                ),
                "candidate_name":
                    f"{application.applicant.user.first_name} "
                    f"{application.applicant.user.last_name}",
                "job_title":
                    application.job.title,
                "match_score":
                    application.total_match_score,
                "status":
                    application.status,
                "applied_date":
                    application.applied_date
            }) 

        return self.success_response(
            message="Dashboard data retrieved successfully",
            data={
                "summary": {
                    "total_jobs": total_jobs,
                    "total_applications": total_applications,
                    "average_match_score": round(
                        average_match_score,
                        2
                    ),
                    "top_candidates": top_candidates
                },
                "applications_per_job": job_chart,
                "match_score_distribution":
                    match_distribution,
                "recent_jobs":
                    recent_jobs_data,
                "recent_applications":
                    recent_applications_data
            }
        )               