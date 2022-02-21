import pytest
from marshmallow import ValidationError
from objects.validator import (
    validate_attribution_type,
    validate_detection_type,
    validate_hash,
    validate_sighting_type,
    validate_version,
)

invalid_hash = "1234567890"
md5_hash = "867D6272792965D11317BFB6308E20A9"
sha1_hash = "cf23df2207d99a74fbe169e3eba035e633b65d94"
sha256_hash = "8C033B3C46767590C54C191AEEDC0162B3B8CCDE0D7B75841A6552CA9DE76044"


def test_validatehash():
    validate_hash(md5_hash)
    validate_hash(sha1_hash)
    validate_hash(sha256_hash)
    with pytest.raises(ValidationError):
        validate_hash(invalid_hash)


def test_validate_version():
    validate_version("1.0")
    with pytest.raises(ValidationError):
        validate_version("bad_version")


def test_validate_sighting_type():
    validate_sighting_type("direct_technique")
    validate_sighting_type("direct_software")
    validate_sighting_type("indirect_software")
    with pytest.raises(ValidationError):
        validate_sighting_type("unknown_thing")


def test_validate_detection_type():
    validate_detection_type("human_validated")
    validate_detection_type("machine_validated")
    with pytest.raises(ValidationError):
        validate_detection_type("unknown_thing")


def test_validate_attribution_type():
    validate_attribution_type("group")
    validate_attribution_type("incident")
    validate_attribution_type("software")
    with pytest.raises(ValidationError):
        validate_attribution_type("unknown_thing")
