from django.core.cache import cache
from django.conf import settings


class BaseOpenCageCache:

    BASE_KEY = "open_cage"
    TIME_TO_LIVE = settings.OPEN_CAGE_CACHE_TIME_TO_LIVE

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def set(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def build_key(self, *args, **kwargs):
        raise NotImplementedError

    def set_to_cache(self, key, response):
        return cache.set(key, response, self.TIME_TO_LIVE)


class ForwardGeocodingCache(BaseOpenCageCache):

    def get(self, query, country):
        key = self.build_key(query, country)
        return cache.get(key)

    def set(self, query, country, response):
        key = self.build_key(query, country)
        return self.set_to_cache(key, response)

    def delete(self, query, country):
        key = self.build_key(query, country)
        return cache.delete(key)

    def build_key(self, query, country):
        return f"{self.BASE_KEY}_forward_geocoding_{query}_{country}"


class ReverseGeocodingCache(BaseOpenCageCache):

    def get(self, latitude, longitude):
        key = self.build_key(latitude, longitude)
        return cache.get(key)

    def set(self, latitude, longitude, response):
        key = self.build_key(latitude, longitude)
        return self.set_to_cache(key, response)

    def delete(self, latitude, longitude):
        key = self.build_key(latitude, longitude)
        return cache.delete(key)

    def build_key(self, latitude, longitude):
        return f"{self.BASE_KEY}_reverse_geocoding_{latitude}_{longitude}"
