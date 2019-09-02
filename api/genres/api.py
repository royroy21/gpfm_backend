from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from api.genres.serializers import GenreSerializer
from genres.models import Genre


class ListGenres(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer = GenreSerializer

    def get(self, request):
        genres = self.serializer(Genre.objects.order_by("name"), many=True)
        return Response(genres.data)
