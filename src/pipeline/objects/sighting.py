from marshmallow import Schema, fields, post_load
from objects.technique import TechniqueSchema
from objects.validator import (
    validate_attribution_type,
    validate_detection_type,
    validate_hash,
    validate_sighting_type,
    validate_version,
)


class Sighting:
    def __init__(
        self,
        version,
        id,
        sighting_type,
        start_time,
        end_time,
        detection_type,
        techniques,
        hash,
        software_name,
        sector,
        country,
        region,
        size,
        attribution_type,
        attribution,
        detection_source,
        privilege_level,
    ):
        self.version = version
        self.id = id
        self.sighting_type = sighting_type
        self.start_time = start_time
        self.end_time = end_time
        self.detection_type = detection_type
        self.techniques = techniques
        self.hash = hash
        self.software_name = software_name
        self.sector = sector
        self.country = country
        self.region = region
        self.size = size
        self.attribution_type = attribution_type
        self.attribution = attribution
        self.detection_source = detection_source
        self.privilege_level = privilege_level

    def __repr__(self):
        time = self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        return "{}({},{},{},{})".format(type(self).__name__, self.id, self.sighting_type, time, self.detection_type)


class SightingSchema(Schema):
    version = fields.Str(validate=validate_version)
    id = fields.Str()
    sighting_type = fields.Str(validate=validate_sighting_type)
    start_time = fields.DateTime()
    end_time = fields.Str(missing=None)  # Some are 00:00T...
    detection_type = fields.Str(validate=validate_detection_type)
    techniques = fields.List(fields.Nested(TechniqueSchema()))
    hash = fields.Str(validate=validate_hash, missing=None)
    software_name = fields.Str(missing=None)
    sector = fields.List(fields.Str(missing=None), missing=None)
    country = fields.Str(missing=None)
    region = fields.Str(missing=None)
    size = fields.Str(missing=None)
    attribution = fields.Str(valdate=validate_attribution_type, missing=None)
    attribution_type = fields.Str(missing=None)
    detection_source = fields.Str(missing=None)
    privilege_level = fields.Str(missing=None)

    @post_load
    def make_sighting(self, data, **kwargs):
        return Sighting(**data)
