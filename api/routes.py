from rest_framework.routers import DefaultRouter

from api.genres.views import GenresViewSet
from api.locations import views as locations_views

api_router = DefaultRouter()

api_router.register(r'genres', GenresViewSet)
api_router.register(
    r'locations/geocoding',
    locations_views.LocationsGeocodingViewSet,
    basename='locations_geocoding',
)
api_router.register(
    r'locations/search',
    locations_views.LocationsSearchViewSet,
    basename='locations_search',
)
