from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from services.tasks import set_price

"""
    тут описуєм моделі (дазу даних)
"""


class Service(models.Model):
    # CharField - для max_length обов'язкове поле
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()  # PositiveIntegerField - вигляді цілого числа

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_full_price = self.full_price

    def save(self, *args, **kwargs):

        if self.__old_full_price != self.full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

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

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)  # max_length - обов'язкове поле
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_discount_percent = self.discount_percent

    def save(self, *args, **kwargs):

        if self.__old_discount_percent != self.discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_plan_type_display()} Plan - {self.discount_percent}% off"

    class Meta:
        verbose_name = "План"
        verbose_name_plural = "Плани"


class Subscription(models.Model):
    # related_name - з яким імям(модель в якій пишемо) вона буде доступна з тою моделю з якою робимо зв'язок(Client)
    # ForeignKey - зв'язок один до багатьох
    # Тут один Client... (One) може мати багато Subscription (Many).
    # нище описуємо зв'язок між моделями
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions', null=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default='')

    def __str__(self):
        return f"{self.client} - {self.service} ({self.plan})"

    class Meta:
        verbose_name = "Підписка"
        verbose_name_plural = "Підписки"
