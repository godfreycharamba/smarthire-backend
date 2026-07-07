import uuid
from django.db import models
from profiles.models import EmployerProfile


class Job(models.Model):

    JOB_TYPES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("closed", "Closed"),
        ("draft", "Draft"),
    ]

    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employer_profile = models.ForeignKey(EmployerProfile,on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True,null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    description = models.TextField()
    required_skills = models.JSONField(default=list,blank=True)
    required_experience = models.JSONField(default=list,blank=True)
    required_education = models.JSONField(default=list,blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft")
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
