import json

import pytest
from marshmallow import ValidationError
from objects.sighting import Sighting, SightingSchema

sighting_model = """
{
    "version": "1.0",
    "id": "DT-1234",
    "sighting_type": "direct_technique",
    "start_time": "2019-01-01T08:12:00Z",
    "end_time": "2019-01-01T08:12:00Z",
    "detection_type": "human_validated",
    "techniques": [
        {
        "technique_id": "T1088",
        "start_time": "2019-01-01T08:12:00Z",
        "end_time": "2019-01-01T08:12:00Z",
        "platform": "Windows 10",
        "raw_data": [
            {"process.create":
            {"command_line": "at 13:30 /interactive cmd"}}
        ]
        }
    ],
    "hash": "a61c66d9c15533fd1d9c6edf7f1d528197724543d1629dfb15f0eb6c222bc453",
    "software_name": "Win32 EXE",
    "sector": ["healthcare"],
    "country": "us",
    "attribution_type": "software",
    "detection_source": "host-based",
    "privilege_level": "none"
}
"""


def test_sighting():
    data = json.loads(sighting_model)
    schema = SightingSchema()
    result = schema.load(data)
    assert isinstance(str(result), str)
    assert isinstance(result, Sighting)
    assert result.techniques[0].technique_id == "T1088"
    assert result.hash == "a61c66d9c15533fd1d9c6edf7f1d528197724543d1629dfb15f0eb6c222bc453"


def test_sighting_validation_version():
    model = sighting_model
    with pytest.raises(ValidationError):
        data = json.loads(model)
        data["version"] = "bad 123"
        result = SightingSchema().load(data)
        assert result.techniqueID == "DT-1234"


def test_sighting_validation_sighting_type():
    model = sighting_model
    with pytest.raises(ValidationError):
        data = json.loads(model)
        data["sighting_type"] = "bad_type"
        result = SightingSchema().load(data)
        assert result.techniqueID == "DT-1234"


def test_sighting_validation_hash():
    model = sighting_model
    with pytest.raises(ValidationError):
        data = json.loads(model)
        data["hash"] = "bad_bash"
        result = SightingSchema().load(data)
        assert result.techniqueID == "DT-1234"


def test_sighting_validation_hash_md5():
    model = sighting_model
    data = json.loads(model)
    data["hash"] = "867D6272792965D11317BFB6308E20A9"
    result = SightingSchema().load(data)
    assert result.hash == "867D6272792965D11317BFB6308E20A9"


def test_sighting_validation_hash_sha1():
    model = sighting_model
    data = json.loads(model)
    data["hash"] = "cf23df2207d99a74fbe169e3eba035e633b65d94"
    result = SightingSchema().load(data)
    assert result.hash == "cf23df2207d99a74fbe169e3eba035e633b65d94"


def test_sighting_validation_hash_sha256():
    model = sighting_model
    data = json.loads(model)
    data["hash"] = "8C033B3C46767590C54C191AEEDC0162B3B8CCDE0D7B75841A6552CA9DE76044"
    result = SightingSchema().load(data)
    assert result.hash == "8C033B3C46767590C54C191AEEDC0162B3B8CCDE0D7B75841A6552CA9DE76044"
