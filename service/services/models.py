from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


# CharField - для max_length обов'язкове поле
class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()  # PositiveIntegerField - вигляді дробу


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ])


class Subscription(models.Model):
    # related_name - з яким імям вона буде доступна з тою моделю з якою робим зв'язок
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
