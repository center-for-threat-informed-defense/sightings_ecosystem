import json

import pytest
from db.model import ModelHelper, SightingTable, TechniqueTable
from objects.sighting import SightingSchema
from objects.technique import TechniqueSchema

import pipeline


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    yield session_
    session_.rollback()
    session_.close()


def test_db_tables():
    s = SightingTable()
    s.id = "1"
    s.sighting_type = "direct-technique-sighting"
    s.start_time = "2019-01-01T08:12:00Z"
    s.end_time = "2019-01-01T08:12:00Z"
    s.detection_type = "human-validated"
    s.software = "Adobe Acrobat 10.1"
    assert isinstance(s, SightingTable)
    s.sighting_type = "direct-software-sighting"
    assert isinstance(s, SightingTable)
    s = TechniqueTable()
    s.technique_id = "T1088"
    s.startTime = "2019-01-01T08:12:00Z"
    s.endTime = "2019-01-01T08:12:00Z"
    s.platform = "Windows 10"
    s.raw_data = '{"process.create":{"command_line": "at 13:30 /interactive cmd"}}'
    assert isinstance(s, TechniqueTable)


def test_model_helper():
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
    technique_model = """
    {
        "technique_id": "T1003",
        "platform": "Windows 10 Enterprise",
        "start_time": "2019-02-01T08:12:00Z",
        "end_time": "2019-02-01T08:12:00Z"
    }
    """
    technique_model_alt = """
    {
        "technique_id": "T1003.001",
        "platform": "Windows 10 Enterprise",
        "start_time": "2019-02-01T08:12:00Z",
        "end_time": "2019-02-01T08:12:00Z",
        "tactic": "Discovery",
        "raw_data": [
        { "process.create": {"command_line": "at 13:30 /interactive cmd"} }
        ]
    }
    """
    data = json.loads(sighting_model)
    schema = SightingSchema()
    objModel = schema.load(data)
    sightingtable = ModelHelper.convert_model_to_sighting_table(objModel)
    assert hasattr(sightingtable, "__class__")
    objModel.sighting_type = "direct_software"
    sightingtable = ModelHelper.convert_model_to_sighting_table(objModel)
    assert hasattr(sightingtable, "__class__")
    schema = TechniqueSchema()
    objModel = schema.load(json.loads(technique_model))
    techniqueTable = ModelHelper.convert_model_to_technique_table(objModel, 1)
    assert hasattr(techniqueTable, "__class__")
    objModel = schema.load(json.loads(technique_model_alt))
    techniqueTable = ModelHelper.convert_model_to_technique_table(objModel, 1)
    assert hasattr(techniqueTable, "__class__")


@pytest.mark.xfail
def test_db_session():
    pipeline.db_session()
