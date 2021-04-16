# Sightings Ecosystem

This project is intended to give cyber defenders unprecedented visibility into what adversaries are actually doing in the wild. With your help, we are tracking MITRE ATT&CK® techniques observed in the wild to give defenders real data on technique prevalence and technique co-occurrence. With this data, we can analyze trends in evolving adversary behaviors, and ultimately provide a data-driven resource to support prioritizing defensive operations. This project will ingest ATT&CK technique sightings and process them to produce useful datasets and reporting. 

You can be a part of the success of this project by contributing your Sightings data and help advance the state of cybersecurity at large. To join us, please email CTID@MITRE-Engenuity.org. 

Take a look at our [data model](./dataModel.md) to have a better understanding of the data we're trying to collect. 

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

## Plan of Attack (no, not that ATT&CK)
This project will be executed in four main phases: contributor engagement, data transformation and analysis, reporting, and process establishment.

- Contributor Engagement — If you’re reading this, this could be you. We need as much support from the community as possible, so do your part and join up now. We will work with you to understand your data and support you in becoming a sightings data contributor.
- Data Transformation & Analysis — Data received by the Center will be anonymized and transformed in a way that provides meaning to each of the sightings we capture. We will establish a data processing pipeline to normalize and prepare your contributions for analysis. We will then create analysis capabilities to identify technique frequency, co-occurrence among techniques, and other topics as the data permits.
- Reporting — We will perform in-depth analysis to the anonymized data and release the results so that the community can have real insights into which techniques are most commonly used, which techniques precede or proceed one another, and where defenders should focus their attention.
- Process Establishment — We will prepare the Center to iteratively analyze sightings data and produce results in the future. We will also enable others to perform analysis of their own data by sharing our methods and tools.

Ultimately, the project will establish the foundation of an ATT&CK sightings ecosystem in which we can routinely collect, analyze, and report on trends in adversary behavior driven by community-wide data contributions.

## Types of Sightings

Sightings data collection will take three forms, each of which provides a different insight into the usage of techniques.

### Direct sighting of a technique

The ATT&CK team is most interested in data from actual sightings of techniques being executed in the course of an attack. In other words, during an event investigation data is collected which shows that one or more ATT&CK techniques were actually used by the adversary on (or targeted at) the victim infrastructure. Cases where multiple techniques were detected as part of a single attack should be reported as a single sighting with multiple techniques listed.

**Example**: If mimikatz were used on a victim machine to dump credentials and that was observed by an EDR tool, it would constitute a direct sighting of Credential Dumping. This might take the form of a sighting of a process accessing lsass.exe memory, for example.

Direct sightings of techniques are the most valuable type of sighting because they tell you, at a ground-truth level, that the adversary relied on a specific technique to carry out an attack.

### Direct sighting of malicious software

In some cases, a technique might not be directly observed (or even be observable given sensing capability) but the presence of a piece of malicious software on the machine can give a strong hint that it was used. In other cases, software to carry out a technique might be blocked at the perimeter – in those cases, it indicates that the adversary might have wanted to use a certain technique but wasn't able to.

*Note: There is of course a grey area when talking about malicious software. What we mean is tools that can be used to carry out malicious attacks, including things commonly called "penetration test" software as well as those that are clearly malicious. On the other hand, we don't mean built-in OS functionality. So please **do** send us sightings of things like metasploit or cobalt strike, but **do not** send us sightings of powershell or the net command. Those latter items should be reported as a direct sighting of a technique (e.g., T1086).*

**Example**: The presence of mimikatz.exe on a machine without evidence that it was actually run to dump credentials – or, mimikatz.exe being blocked at the perimeter or by antimalware -- would constitute a direct sighting of mimikatz. From that, you can assume some attempt to perform credential access techniques available in mimikatz -- but because they were not directly observed, you can't be certain exactly what did or could have happened.

Note that direct software sightings are most useful for [software already contained in ATT&CK](https://attack.mitre.org/software/) that directly enables one or more ATT&CK techniques.

### Indirect sighting of malicious software

In other cases, threat intelligence platforms or ISACs might have data feeds that indirectly demonstrate the fact that a piece of software is being used, without directly observing it.

**Example**: A file hash for mimikatz.exe shared to an ISAC or threat intel platform would be an indirect sighting of mimikatz.exe. As with a direct sighting of malware, this does provide some indication (though weaker) that an adversary was interested in performing credential access.

Note that, as above, indirect software sightings are most useful for [software already contained in ATT&CK](https://attack.mitre.org/software/) that directly enables one or more ATT&CK techniques. Additionally, indirect sightings should only be reported when there is a reasonable presumption that they haven't been reported by another party. In other words, don't write a scraper for some TIP and send sightings for all IOCs in that TIP unless you own or operate the TIP (if you do, please send us the sightings!).

## Notice 

Copyright 2021 MITRE Engenuity. Approved for public release. Document number CT0011

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

This project makes use of ATT&CK®

[ATT&CK Terms of Use](https://attack.mitre.org/resources/terms-of-use/)
