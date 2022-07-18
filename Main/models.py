from datetime import date
from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Files(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    id = models.CharField(max_length=10, primary_key=True, unique=True)

    def __str__(self):
        return self.title