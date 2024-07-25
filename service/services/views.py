from django.db.models import Prefetch, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

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
        # aggregate - вірноситься до ВСІХ Subscription
        # aggregate - виводимо сумарну інформацію по групі записів
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(
            total=Sum('price')).get('total')
        response.data = response_data

        return response
