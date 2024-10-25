from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete will delete a post if a user is deleted
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): #after a new post is created, this defines the redirect route to post-detail(check urls.py)
        return reverse('post-detail', kwargs={'pk':self.pk})
    
