from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #deleting a user will delete their posts and profile.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    logged_in_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self): #resizing the profile images on our site
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 and img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
# should add a field that suspends a user with >5 failed password login attempts

class CustomUser(AbstractUser):
    failed_attempts = models.IntegerField(default = 0)
    is_suspended = models.BooleanField(default = False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password = None):
        User = get_user_model() #this retrieves user 

        try:
            user = User.objects.get(username=username) 
        except:
            user.DoesNotExist
            return None  #if username is invalid, login process stops
        if user.check_password(password):
            user.failed_attempts = 0 #no failed attempts
            return user 
        else:
            user.failed_attempts +=1
            if user.failed_attempts > 5:
               user.is_suspended = True
            user.save()
            return None
        
    def check_and_suspend_user(self):
        profile = Profile.objects.all()
        user = get_user_model()

        if timezone.now - profile.logged_in_time > timedelta(days=30):
            user.is_suspended = True
            user.save()

        
