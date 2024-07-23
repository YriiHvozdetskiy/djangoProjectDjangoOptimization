from celery import shared_task

"""
  таска влаштована так що стоїть в черзі і чикає поки її celery забере 
  на виконання це може заняти якийсь час
  якщо передаєм обєкт subscription за цей час він може змінитися 
"""


@shared_task
def set_price(subscription_id):
    # крос імпорт
    from services.models import Subscription

    subscription = Subscription.objects.get(id=subscription_id)
    new_price = (subscription.service.full_price - subscription.service.full_price
                 * subscription.plan.discount_percent / 100)
    subscription.price = new_price
    subscription.save(save_model=False)
