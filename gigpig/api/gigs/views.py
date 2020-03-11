from rest_framework import authentication, permissions, viewsets

from gigpig.api.gigs.serializers import GigSerializer
from gigpig.gigs import models


class GigViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GigSerializer
    queryset = models.Gig.objects.order_by("-date_created")

    def get_queryset(self):
        gigs_added = self.request.query_params.get('added', None)
        if gigs_added:
            user = self.request.user
            return self.queryset.filter(user=user)

        return super().get_queryset()
