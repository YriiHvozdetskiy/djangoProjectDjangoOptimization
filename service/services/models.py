from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


# CharField - для max_length обов'язкове поле
class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()  # PositiveIntegerField - вигляді дробу

    def __str__(self):
        return f"{self.name} - ${self.full_price}"

    class Meta:
        verbose_name = "Сервіс"
        verbose_name_plural = "Сервіси"


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.get_plan_type_display()} Plan - {self.discount_percent}% off"

    class Meta:
        verbose_name = "План"
        verbose_name_plural = "Плани"


class Subscription(models.Model):
    # related_name - з яким імям вона буде доступна з тою моделю з якою робим зв'язок
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions', null=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')

    def __str__(self):
        return f"{self.client} - {self.service} ({self.plan})"

    class Meta:
        verbose_name = "Підписка"
        verbose_name_plural = "Підписки"
