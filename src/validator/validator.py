"""
    Standalone helper utility to validate data against the Sighting model.

    Usage:
        python3 validator.py -i test_me.json
"""
import argparse
import json
import sys

import jsonschema


def get_argparse():
    desc = "Sightings Validator"
    argparser = argparse.ArgumentParser(description=desc)
    argparser.add_argument("-i", type=str, help="Input to validate")
    return argparser


def validate_document_against_jsonschema(input_path, schema_path):
    """Raises SchemaError or ValidationError Exception if
    there is a problem with the schema or YAML document."""
    with open(input_path, mode="r", encoding="utf-8") as f:
        json_object = json.load(f)

    with open(schema_path, mode="r", encoding="utf-8") as f:
        schema_object = json.load(f)

    jsonschema.validate(json_object, schema_object)


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python3 validator.py -i test_me.json")
        exit(0)

    parser = get_argparse()
    args = parser.parse_args()

    print("[+] Input Document: %s" % (args.i))

    try:
        validate_document_against_jsonschema(args.i, "sighting_schema.json")
        print("[+] Validation Success!")

    except jsonschema.exceptions.ValidationError as error:
        print("[-] Validation Failed!")
        print(error)
