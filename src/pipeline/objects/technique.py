from marshmallow import Schema, fields, post_load


class Technique:
    def __init__(self, technique_id, platform, start_time, end_time, tactic, raw_data):
        self.technique_id = technique_id
        self.platform = platform
        self.start_time = start_time
        self.end_time = end_time
        self.tactic = tactic
        self.raw_data = raw_data

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.technique_id)


class TechniqueSchema(Schema):
    technique_id = fields.Str()
    platform = fields.Str(missing=None)
    start_time = fields.DateTime(missing=None)
    end_time = fields.Str(missing=None)  # Some are 00:00T...
    tactic = fields.Str(missing=None)
    raw_data = fields.List(fields.Dict(), missing=None)

    @post_load
    def make_technique(self, data, **kwargs):
        return Technique(**data)
