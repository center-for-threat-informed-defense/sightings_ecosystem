Data Model
==========

Specfication
------------

We provide a data model for contributors that shows the format for submitting
information and includes required and optional fields. Between Sightings 1.0 and 2.0,
our data model changed slightly with the elimination of ``size``, ``end_time``,
``attribution``, and ``attribution_type`` fields. Size, when combined with data from
other fields, could reveal victim information despite our anonymizing attempts. It is
also a difficult field to collect, like end_time, because contributors likely do not
include this information in their own data collection. Additionally, attribution is a
notoriously difficult problem in the cyber security community. It takes contributors
significant time and effort to identify attribution, if it’s even possible to do.
Because of these considerations and the lack of data for these fields in round 1, we
removed them for round 2. We also added a platform field for round 2. This allowed us to
easily view sightings across different operating systems.

.. list-table:: Sightings Ecosystem data model
    :widths: 20 20 60
    :header-rows: 1

    * - Field
      - Datatype
      - Description
    * - ``version``
      - String
      - Required version string for the data model. **MUST** be set to ``2.0``.
    * - ``id``
      - String
      - Required ID for this event. **MUST** be in UUIDv4 format.
    * - ``start_time``
      - Timestamp
      - Time the activity started, in UTC. **MUST** be in `RFC 3339, section 5.6
        <https://datatracker.ietf.org/doc/html/rfc3339#section-5.6>`__ **date-time**
        format. For example: `2018-11-13T20:20:39+00:00`.
    * - ``tid``
      - Array<String>
      - Array of techniques, including subtechniques that were observed. **MUST**
        contain at least one technique.
    * - ``detection_type``
      - String
      - **MUST** be one of the following values: ``human_validated`` or ``raw``. Use
        ``human_validated`` when a human analyst has reviewed the detection and
        determined it to not be a false positive. Use ``raw`` when no validation has
        occurred.
    * - ``detection_source``
      - String
      - **MUST** be one of the following values: ``host_based``, ``network_based``, or
        ``cloud_based``.
    * - ``software_name``
      - String
      - Malicious software that was observed. **SHOULD** be an exact name from the list
        of `Software Names or Associated Software
        <https://attack.mitre.org/software/>`__ in ATT&CK.
    * - ``hash``
      - String
      - Value **MUST** be MD5, SHA-1, or SHA-256 hash of the software.
    * - ``sector``
      - String
      - **MUST** be 2-digit `NAICS <https://www.census.gov/naics/?58967?yearbck=2022>`__
        code for the sector in which the victim belongs, such as ``22`` ("Utilities").
        If the NAICS code has more than 2 digits, enter only the first 2.
    * - ``country``
      - String
      - **MUST** be the ISO 3166-1 alpha-2 country code of the victim. For example,
        United States is ``us``.
    * - ``region``
      - String
      - **Only submit if not submitting ``country```**. The `IANA Regional Internet
        Registry <https://www.iana.org/numbers>`__ code of the victim, e.g. ``ARIN``.
    * - ``platform``
      - String
      - The platform on which this technique was observed. Valid options are
        ``windows``, ``macos``, ``nix``, or ``other``.
    * - ``privilege_level``
      - String
      - **MUST** be one of the following values: ``system``, ``admin``, ``user``, or
        ``none``.

Examples
--------

This is an example of a sighting with a single technique:

.. code:: json

    {
        "version": "2.0",
        "id": "108b6a04-7140-4bec-bf87-6a9221a2daf0",
        "start_time": "2019-01-01T08:12:00Z",
        "tid": [
            "T1078.003"
        ],
        "detection_type": "human_validated",
        "detection_source": "host_based",
        "sector": "22",
        "country": "us",
        "platform": "windows",
        "privilege_level": "user"
    }

This is an example of a sighting with multiple techniques:

.. code:: json

    {
        "version": "2.0",
        "id": "4c32b581-b463-48c8-9fa9-7a637010c6a8",
        "start_time": "2019-01-01T08:12:00Z",
        "tid": [
            "T1059.001",
            "T1053.003",
            "T1543.002"
        ],
        "detection_type": "human_validated",
        "detection_source": "host_based",
        "sector": "22",
        "country": "fr",
        "platform": "macos",
        "privilege_level": "admin"
    }

JSON Schema
-----------

View the JSON schema in `our project GitHub repository
<https://github.com/center-for-threat-informed-defense/sightings_ecosystem/blob/main/data/sightings2-schema.json>`__.
