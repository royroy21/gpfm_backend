from rest_framework_gis.fields import GeometryField


class GeometryFieldWithDefaultZValue(GeometryField):
    """
    If no z geometry is provided or z geometry is
    None a default value for z of 0.0 will be used.

    Example:
          a) (0.0170409, 51.4875798, None) => (0.0170409, 51.4875798, 0.0)
          b) (0.0170409, 51.4875798) => (0.0170409, 51.4875798, 0.0)
          c) (0.0170409, 51.4875798, 17.0) => (0.0170409, 51.4875798, 17.0)
    """
    def parse_value(self, value):
        return {
            "type": "Point",
            "coordinates": value,
        }

    def convert_coordinates_to_include_z_value(self, value):
        if not isinstance(value, dict):
            return value

        coordinates = value.get("coordinates")
        if not coordinates:
            return value

        value_copy = value.copy()
        if len(coordinates) == 2:
            coordinates.append(0)
            value_copy["coordinates"] = coordinates
            return value_copy

        if coordinates[2] is None:
            coordinates[2] = 0
            value_copy["coordinates"] = coordinates
            return value_copy

        return value_copy

    def to_internal_value(self, value):
        value = self.parse_value(value)
        value = self.convert_coordinates_to_include_z_value(value)
        return super().to_internal_value(value=value)
