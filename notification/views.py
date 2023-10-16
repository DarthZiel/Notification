from rest_framework import viewsets
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionModelViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):

        user = self.request.user
        serializer.save(user=user)
