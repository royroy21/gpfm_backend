import logging


logger = logging.getLogger(__name__)


# TODO - add tests? try reading: it gives back "Reading, Reading" :/
class OpenCageParser:

    TYPE_VILLAGE = "village"
    TYPE_NEIGHBOURHOOD = "neighbourhood"
    TYPE_CITY = "city"
    TYPE_COUNTY = "county"
    TYPE_POSTCODE = "postcode"
    TYPE_TERMINATED_POSTCODE = "terminated_postcode"
    TYPE_STATE_DISTRICT = "state_district"
    TYPE_STATE = "state"
    TYPE_REGION = "region"
    TYPE_ISLAND = "island"
    TYPE_COUNTRY = "country"

    VALID_TYPES = [
        TYPE_VILLAGE,
        TYPE_NEIGHBOURHOOD,
        TYPE_CITY,
        TYPE_COUNTY,
        TYPE_POSTCODE,
        TYPE_TERMINATED_POSTCODE,
        TYPE_STATE_DISTRICT,
        TYPE_STATE,
        TYPE_REGION,
        TYPE_ISLAND,
        TYPE_COUNTRY,
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
                "bounds": result.get("bounds"),
                "geometry": result["geometry"],
                "name": name,
                "type": components_type,
                "raw_components": components,
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
