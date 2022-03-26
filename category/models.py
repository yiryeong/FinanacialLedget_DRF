from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_category')
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name
