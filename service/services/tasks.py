import time

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F

"""
  таска влаштована так що стоїть в черзі і чикає поки її celery забере 
  на виконання це може заняти якийсь час
  якщо передаєм обєкт subscription за цей час він може змінитися 
"""


@shared_task(base=Singleton)
def set_price(subscription_id):
    # крос імпорт
    from services.models import Subscription

    # емулюємо реальні дані (емолюємо розрахунки)
    time.sleep(5)

    subscription = Subscription.objects.filter(id=subscription_id).annotate(
        annotate_price=F('service__full_price') -
                       F('service__full_price') * F('plan__discount_percent') / 100.00).first()

    subscription.price = subscription.annotate_price
    subscription.save()
