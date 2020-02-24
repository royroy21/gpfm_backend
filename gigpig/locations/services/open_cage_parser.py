import logging

from gigpig.locations import models


logger = logging.getLogger(__name__)


class OpenCageParserError(Exception):
    pass


# TODO - add tests? try reading: it gives back "Reading, Reading" :/
class OpenCageParser:

    VALID_TYPES = [
        location_type
        for location_type, _
        in models.Location.TYPES
    ]

    COMPONENT_FIELD_VILLAGE = "village"
    COMPONENT_FIELD_HAMLET = "hamlet"
    COMPONENT_FIELD_TOWN = "town"
    COMPONENT_FIELD_CITY = "city"
    COMPONENT_FIELD_SUBURB = "suburb"
    COMPONENT_FIELD_COUNTY = "county"
    COMPONENT_FIELD_STATE = "state"
    COMPONENT_FIELD_ISLAND = "island"
    COMPONENT_FIELD_COUNTRY = "country"
    COMPONENT_FIELD_POSTCODE = "postcode"

    FORMATTED_NAME_FIELDS = [
        COMPONENT_FIELD_VILLAGE,
        COMPONENT_FIELD_HAMLET,
        COMPONENT_FIELD_TOWN,
        COMPONENT_FIELD_CITY,
        COMPONENT_FIELD_SUBURB,
        COMPONENT_FIELD_COUNTY,
    ]

    FORMATTED_NAME_OVERRIDES = {
        COMPONENT_FIELD_STATE: "state",
        COMPONENT_FIELD_ISLAND: "island",
        COMPONENT_FIELD_COUNTRY: "country",
        COMPONENT_FIELD_POSTCODE: "postcode",
    }

    COUNTRY_CODE_KEY = "ISO_3166-1_alpha-2"

    def parse_results(self, response, query=None):
        names_added = []
        parsed_results = []

        for result in response["results"]:
            components = result["components"]
            components_type = components["_type"]
            if components_type not in self.VALID_TYPES:
                continue

            if query:
                name = self.get_formatted_name_using_query(components, query)
            else:
                name = self.get_formatted_name(components)

            if name in names_added:
                continue

            names_added.append(name)
            parsed_results.append({
                # TODO - implement bounds after geometry
                # "bounds": result.get("bounds"),

                "country": self.get_country_id(components),
                "geometry": [
                    result["geometry"]["lat"],
                    result["geometry"]["lng"],
                ],
                "name": name,
                "type": components_type,
                "components": components,
            })

        return parsed_results

    def get_formatted_name_using_query(self, components, query):
        matching_field = \
            self.get_first_matching_field(components, query)
        if not matching_field:
            logger.debug("no matching field")
            return self.get_formatted_name(components)

        name_override = self.FORMATTED_NAME_OVERRIDES.get(matching_field)
        if name_override:
            return components[name_override]

        logger.debug("matching field is %s", matching_field)
        matching_index = \
            self.FORMATTED_NAME_FIELDS.index(matching_field)
        formatted_name_type_order = [
            field
            for field
            in self.FORMATTED_NAME_FIELDS
            if self.FORMATTED_NAME_FIELDS.index(field) >= matching_index
        ]
        return ", ".join([
            components.get(field)
            for field
            in formatted_name_type_order
            if components.get(field)
        ])

    def get_first_matching_field(self, components, query):
        extra_fields = [
            self.COMPONENT_FIELD_STATE,
            self.COMPONENT_FIELD_ISLAND,
            self.COMPONENT_FIELD_COUNTRY,
            self.COMPONENT_FIELD_POSTCODE,
        ]
        for field in self.FORMATTED_NAME_FIELDS + extra_fields:
            if components.get(field, "").lower().startswith(query.lower()):
                return field

        return None

    def get_formatted_name(self, components):
        return ", ".join([
            components.get(field)
            for field
            in self.FORMATTED_NAME_FIELDS
            if components.get(field)
        ])

    def get_country_id(self, components):
        country_code = components[self.COUNTRY_CODE_KEY]
        country = \
            models.Country.objects.filter(code=country_code.upper()).first()
        if not country:
            raise OpenCageParserError(f"Invalid country code: {country_code}")
        return country.id
