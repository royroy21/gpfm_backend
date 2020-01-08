from rest_framework.routers import DefaultRouter

from api.genres.api import GenreViewSet
from api.locations.api import LocationSearchViewSet


api_router = DefaultRouter()

api_router.register(r'genres', GenreViewSet)
api_router.register(
    r'search/locations', LocationSearchViewSet, basename='search_location')
