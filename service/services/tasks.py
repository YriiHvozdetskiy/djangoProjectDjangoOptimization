import datetime
import time

from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F
from django.conf import settings
from django.core.cache import cache

"""
  таска влаштована так що стоїть в черзі і чикає поки її celery забере 
  на виконання це може заняти якийсь час
  якщо передаєм обєкт subscription за цей час він може змінитися 
"""


# @shared_task - Цей декоратор перетворює функцію на завдання Celery.
# @shared_task - Цей декоратор перетворює функцію на завдання Celery.
# Він дозволяє викликати функцію за допомогою методів Celery, таких як delay()
@shared_task(base=Singleton)
def set_price(subscription_id):
    # крос імпорт
    from services.models import Subscription

    # емулюємо реальні дані (емолюємо розрахунки)
    # time.sleep(5)

    # with transaction.atomic - Це гарантує, що всі операції всередині блоку будуть виконані як одна атомарна транзакція.
    # атомарна - все разом
    with transaction.atomic():
        # select_for_update - забезпечує, що інші транзакції не зможуть змінити цей запис,
        # поки ця транзакція не завершиться.
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=F('service__full_price') -
                            F('service__full_price') * F('plan__discount_percent') / 100.00).first()
        # annotate - вираховуємо значення на рівні бази(щоб не писати ще один prefetch)
        # annotate - вірноситься до КОЖНОГО із Subscription

        subscription.price = subscription.annotated_price
        subscription.save()

    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription
    # with transaction.atomic - Це гарантує, що всі операції всередині блоку будуть виконані як одна атомарна транзакція.
    # атомарна - все разом
    with transaction.atomic():
        # select_for_update - забезпечує, що інші транзакції не зможуть змінити цей запис,
        # поки ця транзакція не завершиться.
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)

        subscription.comment = str(datetime.datetime.now())
        subscription.save()

    cache.delete(settings.PRICE_CACHE_NAME)
