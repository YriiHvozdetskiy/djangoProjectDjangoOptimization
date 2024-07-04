from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from services.models import Subscription, Plan
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # client__user - див пояснення в Notions
    # select_related: для "прямих" зв'язків (ForeignKey, OneToOne),автоматично створює JOIN.
    # prefetch_related: для "зворотних" зв'язків і ManyToMany.
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return Subscription.objects.select_related(
            'plan',
            'client__user'
        ).prefetch_related(
            Prefetch(
                'plan',
                queryset=Plan.objects.all(),
                to_attr='prefetched_plan'
            )
        ).only(
            'id',
            'client__company_name',
            'client__user__email',
            'plan__id',
            'plan__plan_type',
            'plan__discount_percent'
        )
