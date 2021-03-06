import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseOpenCageAPI:

    RATE_LIMIT_ERROR_CODE = 429
    URL = settings.OPEN_CAGE_URL
    RATE_LIMIT_TRIES = settings.OPEN_CAGE_RATE_LIMIT_TRIES
    RATE_LIMIT_WAIT = settings.OPEN_CAGE_RATE_LIMIT_WAIT
    DEFAULT_PARAMETERS = {
        "key": settings.OPEN_CAGE_TOKEN,
    }

    def resolve_query(self, *args, **kwargs):
        raise NotImplementedError

    def get_location_data(self, url, params):
        for rate_limit_try in range(1, self.RATE_LIMIT_TRIES + 1):
            response = self.make_call(url, params)

            if not response.ok:
                if self.has_hit_rate_limit(response):
                    logger.warning(
                        "rate limit hit for call: %s %s (%s/%s)",
                        url,
                        params,
                        rate_limit_try,
                        self.RATE_LIMIT_TRIES,
                    )
                    continue

                logger.error(
                    "problem making call: %s %s response received: %s",
                    url,
                    params,
                    response.text,
                )
                return False
            else:
                return response.json()

        return False

    def make_call(self, url, params):
        params_with_defaults = {
            **self.DEFAULT_PARAMETERS,
            **params,
        }
        return requests.get(url, params=params_with_defaults)

    def has_hit_rate_limit(self, response):
        return response.status_code == self.RATE_LIMIT_ERROR_CODE


class ForwardGeocodingOpenCageAPI(BaseOpenCageAPI):

    RESULTS_LIMIT = 50

    def resolve_query(self, query, country):
        params = {
            "abbrv": 1,
            "countrycode": country,
            "no_dedupe": 1,
            "no_annotations": 1,
            "limit": self.RESULTS_LIMIT,
            "q": query,
        }
        response = self.get_location_data(self.URL, params)
        return response


class ReverseGeocodingOpenCageAPI(BaseOpenCageAPI):

    def resolve_query(self, latitude, longitude):
        params = {
            "abbrv": 1,
            "no_annotations": 1,
            "q": f"{latitude}+{longitude}",
        }
        # TODO - q params gets encoded incorrectly here so no results are returned.
        # See: https://stackoverflow.com/questions/23496750/how-to-prevent-python-requests-from-percent-encoding-my-urls/23497912
        response = self.get_location_data(self.URL, params)
        return response
