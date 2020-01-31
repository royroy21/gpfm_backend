from rest_framework import authentication, permissions, viewsets

from gigpig.api.genres.serializers import GenreSerializer
from gigpig.genres import models


class GenresViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GenreSerializer
    queryset = models.Genre.objects.order_by("-name")
