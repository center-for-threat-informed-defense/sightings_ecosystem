from objects.technique import Technique
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class SightingTable(base):
    __tablename__ = "sighting"
    __table_args__ = {"extend_existing": True}
    sighting_pid = Column(Integer, Sequence("sighting_seq"), primary_key=True)
    id = Column(String, unique=False)
    sighting_type = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    detection_type = Column(String, nullable=False)
    software = Column(String)
    hash = Column(String)
    cid = Column(String, nullable=True)


class TechniqueTable(base):
    __tablename__ = "technique"
    __table_args__ = {"extend_existing": True}
    technique_pid = Column(Integer, Sequence("technique_seq"), primary_key=True)
    technique_id = Column(String, nullable=False)
    sub_technique_id = Column(String)
    platform = Column(String)
    start_time = Column(DateTime)
    tactic = Column(String)
    raw_data = Column(String)
    sighting_id = Column(Integer)


class ModelHelper:
    def convert_model_to_sighting_table(obj):
        s = SightingTable()
        s.id = obj.id
        s.sighting_type = obj.sighting_type
        if obj.start_time:
            s.start_time = obj.start_time
        s.detection_type = obj.detection_type
        if "direct_software" == obj.sighting_type:
            s.software = obj.software_name
        else:
            s.software = ""
        if hasattr(obj, "hash"):
            s.hash = obj.hash
        return s

    def convert_model_to_technique_table(obj, sighting_id):
        t = TechniqueTable()
        if isinstance(obj, Technique):
            technique_split = obj.technique_id.split(".")
            t.technique_id = technique_split[0]
            if len(technique_split) == 2:
                t.sub_technique_id = technique_split[1]
            if obj.platform:
                t.platform = obj.platform
            if obj.start_time:
                t.start_time = obj.start_time
            if obj.tactic:
                t.tactic = obj.tactic
            if obj.raw_data:
                t.raw_data = obj.raw_data
            t.sighting_id = sighting_id
        return t
