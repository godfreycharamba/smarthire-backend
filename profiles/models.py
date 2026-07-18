from django.db import models
from accounts.models import CustomUser
import uuid


class JobSeekerProfile(models.Model):
    PROCESSING_STATUS = (
        ("pending","Pending"),
        ("processing","Processing"),
        ("completed","Completed"),
        ("failed","Failed"),
    )

    profile_id = models.UUIDField(primary_key=True,default=uuid.uuid4 , editable=False, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic_url = models.URLField(blank=True, null=True)
    resume_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    experience = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    processing_status = models.CharField(max_length=20,choices=PROCESSING_STATUS,default="pending")
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
    
class ResumeEmbedding(models.Model):
    embedding_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    profile = models.OneToOneField(JobSeekerProfile,on_delete=models.CASCADE,related_name="embedding")
    skills_embedding = models.JSONField(default=list)
    experience_embedding = models.JSONField(default=list)
    education_embedding = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Embeddings - {self.profile.user.email}"    
