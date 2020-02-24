from rest_framework import authentication, permissions, viewsets

from gigpig.api.gigs.serializers import GigSerializer
from gigpig.gigs import models


class GigViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GigSerializer
    queryset = models.Gig.objects.order_by("-title")
