from django.db import models
from django.utils import timezone
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import jsonfield
# Post Table DataBase
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class AliceBlueApi(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    alice_blue_api=models.CharField(max_length=1000)    


class portfolioDb(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    compnay=jsonfield.JSONField()

# class CustomUser(AbstractUser):
#     alice_blue_api=models.CharField(max_length=1000)    