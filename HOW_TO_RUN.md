[![codecov](https://codecov.io/gh/center-for-threat-informed-defense/sightings/branch/main/graph/badge.svg?token=OK0UGC4LD5)](https://codecov.io/gh/center-for-threat-informed-defense/sightings)

# ATT&CK Sightings

Private research and development repository that supports the public Sightings Ecosystem Project.

The [ATT&CK Sightings project](https://attack.mitre.org/resources/sightings/) is intended to provide cybersecurity defenders and researchers with critical insight into real-world, "in the wild adversary" behaviors mapped to ATT&CK. This project aims to fundamentally advance our collective ability to see threat activity across organizational, platform, vendor, and geographical boundaries. It will collect voluntarily contributed raw “sightings”, or observations, of specific adversary TTPs mapped to ATT&CK, anonymize and aggregate them, and then produce intelligence reports describing insights from that data.

- [ATT&CK Sightings](#attck-sightings)
  - [Install Dependencies](#install-dependencies)
  - [Clone Git Repository](#clone-git-repository)
  - [Quickstart](#quickstart)
  - [Use the Pipeline to Ingest Data](#use-the-pipeline-to-ingest-data)
    - [Run Pipeline Application](#run-pipeline-application)
    - [View Pipeline Logs](#view-pipeline-logs)
    - [Stop Pipeline Application](#stop-pipeline-application)
  - [Analyzing Sightings Data](#analyzing-sightings-data)
    - [Run Analysis Application](#run-analysis-application)
    - [View Analysis Logs](#view-analysis-logs)
    - [Stop Analysis Application](#stop-analysis-application)
  - [Developer Tips](#developer-tips)
    - [Build and Push Updated Container Images](#build-and-push-updated-container-images)
    - [Build container images locally (optional)](#build-container-images-locally-optional)
    - [Using PGAdmin (optional)](#using-pgadmin-optional)
  - [Questions and Feedback](#questions-and-feedback)
  - [Notice](#notice)

## Install Dependencies

- Install docker
  - <https://docs.docker.com/get-docker/>
- Install docker-compose
  - <https://docs.docker.com/compose/install/>

## Clone Git Repository

Next, clone the Sightings Ecosystem repo:

```sh
git clone git@github.com:center-for-threat-informed-defense/sightings_ecosystem.git
cd sightings_ecosystem
```

## Quickstart

1. Assuming the following pre-requisites have been met: 
   1. Docker installed
   2. Sightings JSON files in the `./data/` directory
   3. Command line prompt at root of the git repository
2. Run `make start-pipeline` to process data. 
   1. The processing make take a while depending on amount of data being processed and system resources (e.g. 10 minutes - 8 hours). While the pipeline application is running, it will periodically print out time estimates stating how much data has been processed, and a rough estimate of how much time is remaining, such as `Estimate 8.45 min. to insert 584,595 remaining Sightings`.
   2. Run `make logs` to view the logs and see the most recent status message (`make logs-follow` will tail the log file continously).
3. Once all data has been analyzed, run `make start-analysis` to launch the Analysis web application.
   1. Navigate to <http://localhost:8050> to load the application in your web browser.
4. Success!

## Use the Pipeline to Ingest Data

### Run Pipeline Application

Ingest Process

To use the pipeline application to ingest data, follow the instructions below.

NOTE: By default, the `./data` directory in the current working directory will be processed. To use a different data directory, set the `INPUT_DATA_DIR` environment variable to the desired directory. 

For example:
`declare -x INPUT_DATA_DIR="/path/to/my/data"` will ingest data in the directory `/path/to/my/data` on your host system (path should be on your host system, i.e. Windows/Mac/Linux desktop).

```sh
make start-pipeline
```

### View Pipeline Logs

After starting the application, you can view the logs for errors by running the following in a new terminal window/tab:

```sh
make logs
```

You can also use `docker logs -f <CONTAINER ID>` command, and retrieve the `CONTAINER_ID` value from the output of `docker ps`.

> Please note no output will be printed to screen if logs are empty.

### Stop Pipeline Application

Finally, after ingesting all the data, stop the container if it's still running:

```sh
make stop
```

## Analyzing Sightings Data

Instructions for running the Sightings analysis tool

### Run Analysis Application

> Please note you [need start the database](#start-the-database) and then wait
> until the database is ready to accept connections.

```sh
make start-analysis
```

Wait for Dash to start. Once successful, use your browser to go to `http://localhost:8050/`.

> Note that testing was done with the Google Chrome browser.

### View Analysis Logs

After starting the application, you can view the logs for errors by running the following in a new terminal window/tab:

```sh
make logs
```

You can also use `docker logs -f <CONTAINER ID>` command, and retrieve the `CONTAINER_ID` value from the output of `docker ps`.

> Please note no output will be printed to screen if logs are empty.

### Stop Analysis Application

Finally, to stop the Sightings analysis container if it's still running:

```sh
make stop-analysis
```

## Developer Tips

### Build and Push Updated Container Images

The official container build/push process is handled via Github Actions automation. A new container image is built upon a release of the project being published.

To trigger a new build, follow the steps below:

1. Navigate to the [project's Releases page](https://github.com/center-for-threat-informed-defense/sightings/releases).
2. Create a new release.
   1. Specify a appropriate release version (e.g. `v0.1.0`, `v1.0.0`)
   2. Publish the release.
3. That's it! The CI process will automatically build and post the updated container images. The new images will be tagged with `latest`, as well as the version tag applied earlier (e.g. `sightings-analysis:latest` and `sightings-analysis:v0.1.0` will both be created.)

### Build container images locally (optional)

By default, the application uses the official images published on Github Container Registry. To build your own container images (for development or testing), use the instructions below.

To build local images for the application containers, run the following command:

```sh
make build-containers
```

### Using PGAdmin (optional)

Launch pgadmin by running the following command:

```sh
make start-pgadmin
```

Once launched, one can connect to the pgadmin administrative web interface as follows:

```txt
http://127.0.0.1:80
```

The default credentials are:

```txt
User: sightings@mitre-engenuity.org
Password: sightings
```

Within the pgadmin web interface one can establish a connection to the DB as follows:

- Click on Add Server and provide a name, such as `Sightings`
- Under connections, enter the value: `postgres`
- Authentication: Username/password are `sightings/sightings`

## Questions and Feedback

Please submit issues for any technical questions/concerns or contact ctid@mitre-engenuity.org directly for more general inquiries.

Also see the [guidance for contributors](./CONTRIBUTING.md) if are you interested in contributing or simply reporting issues.

## Notice

Copyright 2021 MITRE Engenuity. Approved for public release. Document number XXXXX

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
