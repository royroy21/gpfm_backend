from rest_framework_gis.fields import GeometryField as DRFGisGeometryField


class GeometryField(DRFGisGeometryField):

    _type = "Point"

    def to_internal_value(self, value):
        return super().to_internal_value(value={
            "type": self._type,
            "coordinates": value,
        })
