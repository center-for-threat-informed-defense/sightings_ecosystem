-- Create required tables on startup if necessary

CREATE SEQUENCE sighting_seq;
CREATE SEQUENCE technique_seq;

CREATE TABLE IF NOT EXISTS sighting
(
    sighting_pid   INTEGER   NOT NULL
        PRIMARY KEY,
    id             VARCHAR,
    sighting_type  VARCHAR   NOT NULL,
    start_time     TIMESTAMP NOT NULL,
    detection_type VARCHAR   NOT NULL,
    software       VARCHAR,
    hash           VARCHAR,
    cid            VARCHAR
);

CREATE TABLE IF NOT EXISTS technique
(
    technique_pid    INTEGER NOT NULL
        PRIMARY KEY,
    technique_id     VARCHAR NOT NULL,
    sub_technique_id VARCHAR,
    platform         VARCHAR,
    start_time       TIMESTAMP,
    tactic           VARCHAR,
    raw_data         VARCHAR,
    sighting_id      INTEGER
);
