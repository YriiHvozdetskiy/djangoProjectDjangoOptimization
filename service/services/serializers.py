from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source='client.company_name')  # source - бачити яка компанія
    email = serializers.CharField(source='client.user.email')
    # SerializerMethodField - серіалізатор шукає таку функцію з префіксом get (наведи і прочитай)
    price = serializers.SerializerMethodField()

    # instance - конкретна підписка
    def get_price(self, instance):
        return (instance.service.full_price
                - instance.service.full_price * (instance.plan.discount_percent / 100))

    class Meta:
        model = Subscription
        # 1.fields - можна вказувати поля які в Subscription (client, service, plan)
        # 2.fields - можна вказувати поля які ми описали в SubscriptionSerializer (сlient_name, email)
        """
         plan_id - скрито в plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
         але ми можем до нього звитратися тут.
        """
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')
