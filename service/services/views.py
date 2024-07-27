from django.db.models import Prefetch, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.conf import settings
from django.core.cache import cache

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # client__user - див пояснення в Notions
    # select_related: для "прямих" зв'язків (ForeignKey, OneToOne),автоматично створює JOIN.
    # prefetch_related: для "зворотних" зв'язків і ManyToMany.
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch(
            'client',
            queryset=Client.objects.all().select_related('user').only('company_name',
                                                                      'user__email'),
        )
    )
    serializer_class = SubscriptionSerializer

    # зробили це щоб додати ще дані на одному рівні з result (перевизначання)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        # в ключ можуть класти ід для якого юзера цей кеш
        # settings - імпортуємо з django.conf, тому що в звичайних settings можуть змінюватися взалежності від середовища
        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            # aggregate - вірноситься до ВСІХ Subscription
            # aggregate - виводимо сумарну інформацію по
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data}
        response_data['total_amount'] = total_price
        response.data = response_data

        return response
