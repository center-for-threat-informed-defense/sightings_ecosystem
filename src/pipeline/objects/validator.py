import re

from marshmallow import ValidationError


def validate_version(s):
    if s != "1.0":
        raise ValidationError("Invalid version information.")


def validate_sighting_type(s):
    if s != "direct_technique" and s != "direct_software" and s != "indirect_software" and s != "software_name":
        raise ValidationError("Invalid sighting_type.")


def validate_detection_type(s):
    if s != "human_validated" and s != "machine_validated" and s != "raw":
        raise ValidationError("Invalid detection_type.")


def validate_attribution_type(s):
    if s != "group" and s != "incident" and s != "software":
        raise ValidationError("Invalid attribution_type.")


HASH_TYPE_REGEX = {
    re.compile(r"^[a-f0-9]{32}(:.+)?$", re.IGNORECASE): [
        "MD5",
        "MD4",
        "MD2",
        "Double MD5",
        "LM",
        "RIPEMD-128",
        "Haval-128",
        "Tiger-128",
        "Skein-256(128)",
        "Skein-512(128",
        "Lotus Notes/Domino 5",
        "Skype",
        "ZipMonster",
        "PrestaShop",
    ],
    re.compile(r"^[a-f0-9]{40}(:.+)?$", re.IGNORECASE): [
        "SHA-1",
        "Double SHA-1",
        "RIPEMD-160",
        "Haval-160",
        "Tiger-160",
        "HAS-160",
        "LinkedIn",
        "Skein-256(160)",
        "Skein-512(160)",
        "MangoWeb Enhanced CMS",
    ],
    re.compile(r"^[a-f0-9]{64}(:.+)?$", re.IGNORECASE): [
        "SHA-256",
        "RIPEMD-256",
        "SHA3-256",
        "Haval-256",
        "GOST R 34.11-94",
        "GOST CryptoPro S-Box",
        "Skein-256",
        "Skein-512(256)",
        "Ventrilo",
    ],
}


def validate_hash(s):
    found = False
    for algorithm in HASH_TYPE_REGEX:
        if algorithm.match(s):
            found = True
    if not found and s != "0":
        raise ValidationError("Invalid hash.")
