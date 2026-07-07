import uuid
from django.db import models

from jobs.models import Job
from profiles.models import JobSeekerProfile


class Application(models.Model):

    STATUS_CHOICES = [
        
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("interview", "Interview"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    ]

    application_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job,on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(JobSeekerProfile,on_delete=models.CASCADE,related_name="applications")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="submitted")
    skills_score = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    experience_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    education_score = models.DecimalField(max_digits=5,decimal_places=2, default=0.00)
    total_match_score = models.DecimalField(max_digits=5,decimal_places=2, default=0.00)
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant.user.email} - {self.job.title}"
