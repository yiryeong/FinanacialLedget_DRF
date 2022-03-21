from django.db import models
from django.contrib.auth.models import User
from category.models import Category


class Expenditure(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_expenditure')
    cid = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenditure_category')
    pay_date = models.DateTimeField()
    price = models.IntegerField()
    place = models.CharField(max_length=45, null=True, blank=True)
    memo = models.CharField(max_length=200, null=True, blank=True)
