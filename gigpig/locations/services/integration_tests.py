import threading

from gigpig.locations import services


class TestLocationIQRateLimiting:
    """
    Tests if service keeps retrying if rate limit is reached.

    This test is intended to be run manually and should not
    run through Django's test suit.
    """
    service = services.ForwardGeocodingOpenCageAPI()
    query_keywords = [
        "charlton",
        "woolwich",
        "bexley",
        "new cross",
        "holloway",
    ]

    def write_location_to_store(self, store, query, country):
        response = self.service.resolve_query(query, country)
        if response:
            store.update({query: response})

    def run_test(self):
        function_args = [
            (query_keyword, "gb")
            for query_keyword
            in self.query_keywords
        ]
        store = {}
        threads = []
        for args in function_args:
            query, country = args
            request = threading.Thread(
                target=self.write_location_to_store,
                args=(store, query, country),
            )
            threads.append(request)
            request.start()

        for thread in threads:
            thread.join()

        errors = [
            f"service did not retrieve data for {keyword}"
            for keyword
            in self.query_keywords
            if keyword not in store
        ]
        if errors:
            print("test failed")
            for error in errors:
                print(error)
        else:
            print("test passed")
