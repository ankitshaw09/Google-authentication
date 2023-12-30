from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from google.oauth2 import service_account

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key = True, on_delete = models.CASCADE)
    credential = models.BinaryField(null=True)
    task = models.CharField(max_length = 80, null = True)
    updated_time = models.CharField(max_length = 80, null = True)

class CredentialsAdmin(admin.ModelAdmin):
    pass