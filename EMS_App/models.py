from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email is not given')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')
        
        return self.create_user(email,password,**extra_fields)
        

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=254,null=False)
    first_name = models.CharField(max_length=255,null=False,blank=False)
    last_name = models.CharField(max_length=255,null=False,blank=False)
    phone = models.IntegerField(null=True,blank=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    def has_module_perms(self,app_label):
        return True
    
    def has_perm(self,perm,obj=None):
        return True
    
    def get_all_permissions(self, obj=None):
        # Implement logic to get all permissions for this user
        return []
    
event_status = (
    ("Not Yet Started","Not Yet Started"),
    ("Processing","Processing"),
    ("Completed","Completed"),
    ("Cancelled","Cancelled")
)

class Events(models.Model):
    customer  = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=50,null=False,blank=False)
    description = models.CharField(max_length=300,null=False,blank=False)
    startdate = models.DateTimeField((""), auto_now=False, auto_now_add=False)
    enddate = models.DateTimeField((""), auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=200,null=False,blank=False)
    organizer = models.CharField(max_length=50,null=False,blank=False)
    status = models.CharField(choices=event_status,max_length=150,default='Not Yet Started',null=False)

    def __str__(self):
        return self.title