from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.forms import BooleanField


class UserAccountManager(BaseUserManager):
    
    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError('User must have email address')
        
        email = self.normalize_email(email)
        #Manager class has an attribute .model
        user= self.model(email=email,name=name)
        user.set_password(password)
        #if you have more than one db use self._db
        user.save()
        return user

    #from manager classes, defining user and superuser fields
    #will be providing the password
    def create_superuser(self, email, name, password):
        user = self.create_user(email,name,password)
        
        user.is_superuser= True
        user.is_staff = True
        user.save()
        
        return user
    
    
    
#create custom user model
class UserAccount(AbstractBaseUser, PermissionsMixin):
    
    #authenticate user by email
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    #custom user account manager
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['name']
    
    #methods from User class
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    
    
    


