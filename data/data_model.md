## Data Model Format Definitions

All formats are JSON and consist of either a list of entries or a single entry. Please e-mail <ctid@mitre-engenuity.org> with any questions or suggestions.

Please do not include any information beyond that specified in the format below. In particular, we do not want to collect sensitive victim information or other PII.

## Sighting

| Field | Datatype | Description |
| ------------------ | -------------- |------------- |
| version        | String         | Required version string for the data model. **MUST** be set to **`2.0`**  |
| id             | String         | Required ID for this event. **MUST** be in UUIDv4 format |
| start_time     | [Timestamp](https://tools.ietf.org/html/rfc3339#page-10)      | Time the activity started, in UTC. **MUST** be in [RFC 3339, section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) **date-time** format. For example: `2018-11-13T20:20:39+00:00` | 
| technique     | Array | Array of techniques, including subtechniques that were observed. One or many techniques can be accepted|
| tactic     | String | \*\***Only if available\*\*** The tactic to which the technique belongs, under the context of this detection. For example, if `Scheduled Jobs` was detected as a means to get system access, this would be `Privilege Escalation`, and not `Persistence`.|
| detection_type | String         | **MUST** be one of the following values: `human_validated` or `raw`. Use `human_validated` when a human analyst has reviewed the detection and determined it to not be a false positive. Use `raw` when no validation has occurred. |
| detection_source   | String         | **MUST** be one of the following values: `host_based`, `network_based`, or `cloud_based` |
| software_name | String | \*\***Only if available**\*\* Malicious software that was observed. **SHOULD** ideally be an exact name from the list of [Software Names or Associated Software](https://attack.mitre.org/software/) already in ATT&CK |
| hash | String | \*\***Only if available**\*\*. Value **MUST** be MD5, SHA-1, or SHA-256 hash of the software|
| sector  | String | **MUST** be [NAICS](https://www.census.gov/naics/?58967?yearbck=2022) code for the sector(s) in which the victim belongs, such as `22`(utilities). \*Only include the first 2 digits |
| country | String | **MUST** be the ISO 3166-1 alpha-2 country code of the victim. For example, United States is `us` |
| region | String  | **Only submit if not submitting `country`**. The [IANA Regional Internet Registry](https://www.iana.org/numbers) code of the victim, e.g. `ARIN`  |
|platform | String | The platform on which this technique was observed. Valid options are `windows`, `macos`, `nix`, `other` |
| privilege_level | String | **MUST** be one of the following values: `system`, `admin`, `user`, `none`  |

## Sightings Examples

### Example Technique Sighting

```json
{
  "version": "2.0",
  "id": "108b6a04-7140-4bec-bf87-6a9221a2daf0",
  "start_time": "2019-01-01T08:12:00Z",
  "technique": [
    "T1078.003"
  ],
  "tactic": "TA004",
  "detection_type": "human_validated",
  "detection_source": "host_based",
  "sector": "22",
  "country": "us",
  "platform": "windows",
  "privilege_level": "user"
}

```

### Example Multiple Techniques in one Sighting

```json
{
  "version": "2.0",
  "id": "4c32b581-b463-48c8-9fa9-7a637010c6a8",
  "start_time": "2019-01-01T08:12:00Z",
  "technique": [
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

```

