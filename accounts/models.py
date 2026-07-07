from django.db import models
from django.contrib.auth.models import AbstractUser , AbstractBaseUser , PermissionsMixin, BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self , email , password = None , **extra_fields):

        # ENSURE EMAIL IS PROVIDED
        if not email:
            raise ValueError("The email field is required")

       
        # NOMALISE EMAIL (LOWER CASE DOMAIN)
        email = self.normalize_email(email)
        user = self.model(email = email , **extra_fields)

        # hashing the password
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self , email, password= None , **extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        return self.create_user(email, password , **extra_fields)

    def create_admin(self , email , password=None , **extra_fields):
        extra_fields.setdefault('is_staff' , True) 
       
        return self.create_user(email , password , **extra_fields) 
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker','Job Seeker'),
        
        ('employer','Employer'),
    )
   
    username = None
    id = models.UUIDField(default=uuid.uuid4 , unique = True , primary_key=True , editable=False)
    first_name = models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)
    email =  models.EmailField(unique=True)
    role =  models.CharField(max_length=100 , choices=ROLE_CHOICES , default='job_seeker')
    phone_number =  models.CharField(max_length=15)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name' , 'last_name' , 'phone_number']
    objects = CustomUserManager() 

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'    
