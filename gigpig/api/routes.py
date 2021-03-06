from rest_framework.routers import DefaultRouter

from gigpig.api.gigs.views import GigViewSet
from gigpig.api.genres.views import GenresViewSet
from gigpig.api.locations import views as locations_views

api_router = DefaultRouter()

api_router.register(r'countries', locations_views.CountryViewSet)
api_router.register(r'gigs', GigViewSet)
api_router.register(r'genres', GenresViewSet)
api_router.register(r'locations', locations_views.LocationViewSet)
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
