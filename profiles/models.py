from django.db import models
from accounts.models import CustomUser
import uuid


class JobSeekerProfile(models.Model):
    profile_id = models.UUIDField(primary_key=True,default=uuid.uuid4 , editable=False, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic_url = models.URLField(blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    experience = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"JobSeekerProfile - {self.user.email}"


class EmployerProfile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4 ,editable=False, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    company_logo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
