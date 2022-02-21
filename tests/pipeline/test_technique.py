import json

from objects.technique import Technique, TechniqueSchema

technique_model = """
{
    "technique_id": "T1003",
    "platform": "Windows 10 Enterprise",
    "start_time": "2019-02-01T08:12:00Z",
    "end_time": "2019-02-01T08:12:00Z"
}
"""


def test_technique():
    data = json.loads(technique_model)
    schema = TechniqueSchema()
    result = schema.load(data)
    assert isinstance(str(result), str)
    assert isinstance(result, Technique)
