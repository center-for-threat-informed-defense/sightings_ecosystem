# Sightings Ecosystem

This project is intended to give cyber defenders visibility into what adversaries are actually doing in the wild. With your help, we are tracking MITRE ATT&CK® techniques observed to give defenders real data on technique prevalence. With this data, we can analyze trends in evolving adversary behaviors, and ultimately provide a data-driven resource to support prioritizing defensive operations. This project ingests ATT&CK technique sightings and process them to produce useful datasets and reporting.

You can be a part of the success of this project by contributing your Sightings data and help advance the state of cybersecurity at large. To join us, please email CTID@MITRE-Engenuity.org.

- [Why Sightings?](#why-sightings)
- [Call for Contributors](#call-for-contributors)
- [Plan of Attack](#plan-of-attack)
- [Example sighting of a technique](#example-sighting-of-a-technique)
- [Notice](#notice)

## Why Sightings?

Defenders need data driven answers to questions like:

- How do I know which techniques to prioritize?
- As a company in the finance sector, do the attackers I face use different tactics from those facing retail or healthcare?
- How are attacks trending over time? Are older forms of attacks still in use?
- Which techniques should I expect to see preceding and proceeding a specific attack?

We believe that a different type of cyber threat intelligence must be shared in order to serve this purpose, and the Center is well-positioned to work across industry. Specifically, security teams, vendors, ISACs/ISAOs, and governments should begin to share sightings of ATT&CK techniques. In other words, they should share when they see adversaries use specific behaviors against real production systems and networks.

## Call for Contributors

Our initial pilot was successful in large part because some of you stepped forward and contributed data that we used to validate our basic premise — that in sufficient quantity (and quality), technique sightings can give defenders a whole new way of understanding what adversaries are doing currently. Based on this initial success we are scaling up and now we need YOU to make this project successful. While we already have some contributors onboard, we need increased community participation to realize our goal. The more contributors, the larger the data set, the better and more useful the results. With each new contributor that joins the Sightings Ecosystem, we can increase the efficacy of Sightings and provide defenders with a more effective tool for their proverbial toolkit.

Outside of benefitting the community at large, there is an added benefit of being a data contributor. As a data contributor, you will have access to a private set of anonymized data that will enable you to perform your own research. This can help you fine tune your own tools and provide a more secure environment for your company or your constituents.

## Plan of Attack

This project will be executed in four main phases: contributor engagement, data transformation and analysis, reporting, and process establishment.

- Contributor Engagement — If you’re reading this, this could be you. We need as much support from the community as possible, so do your part and join up now. We will work with you to understand your data and support you in becoming a sightings data contributor.
- Data Transformation & Analysis — Data received by the Center will be anonymized and transformed in a way that provides meaning to each of the sightings we capture. We will establish a data processing pipeline to normalize and prepare your contributions for analysis. We will then create analysis capabilities to identify technique frequency, co-occurrence among techniques, and other topics as the data permits.
- Reporting — We will perform in-depth analysis to the anonymized data and release the results so that the community can have real insights into which techniques are most commonly used, which techniques precede or proceed one another, and where defenders should focus their attention.
- Process Establishment — We will prepare the Center to iteratively analyze sightings data and produce results in the future. We will also enable others to perform analysis of their own data by sharing our methods and tools.

Ultimately, the project will establish the foundation of an ATT&CK sightings ecosystem in which we can routinely collect, analyze, and report on trends in adversary behavior driven by community-wide data contributions.

## Example sighting of a technique

The ATT&CK team is most interested in data from sightings of techniques being executed in the course of an attack. In other words, during an event investigation data is collected which shows that one or more ATT&CK techniques were actually used by the adversary on (or targeted at) the victim infrastructure. Cases where multiple techniques were detected as part of a single attack should be reported as a single sighting with multiple techniques listed.

**Example**: If mimikatz were used on a victim machine to dump credentials and that was observed by an EDR tool, it would constitute a direct sighting of Credential Dumping. This might take the form of a sighting of a process accessing lsass.exe memory, for example.

## Notice

Copyright 2021 MITRE Engenuity. Approved for public release. Document number CT0022

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
