from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='client')
    company_name = models.CharField(max_length=100)
    full_address = models.CharField(max_length=100)
