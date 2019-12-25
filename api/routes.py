from rest_framework.routers import DefaultRouter

from api.locations.api import LocationViewSet


api_router = DefaultRouter()
api_router.register(
    r'search/locations',
    LocationViewSet,
    basename='search_location',
)
