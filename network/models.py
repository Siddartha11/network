from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Post(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner")
    text=models.TextField()
    likes=models.IntegerField()
    dislikes=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Following(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name="following")
    following_user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

