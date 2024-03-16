Introduction
============

Background
----------

Adversaries are constantly evolving their attacks, driving up the cost of intrusions.
Consequently, defenders must continue to protect against an increasing amount of
adversary techniques and behaviors. Despite their best efforts, it is not possible to
defend against all potential scenarios. This raises the questions, “How many MITRE
ATT&CK techniques apply to the average organization?” and “Which techniques does an
organization realistically need to defend against?”

MITRE’s Center for Threat-Informed Defense (the Center) began addressing these questions
with the Sightings Ecosystem. This project focuses on creating an anonymous,
community-sourced repository of technique detections to identify when and where ATT&CK
techniques occurred in the wild. The Center, in collaboration with `AttackIQ <https://www.attackiq.com/>`__, `Cyber
Threat Alliance <https://www.cyberthreatalliance.org/>`__, `Fortinet’s FortiGuard Labs <https://www.fortinet.com/fortiguard/labs>`__, `HCA Healthcare <https://hcahealthcare.com/>`__, `JP Morgan Chase <https://www.jpmorganchase.com/>`__, and
`Verizon Business <http://www.verizon.com/business>`__, analyzed over 1 million security events that have been mapped to MITRE ATT&CK. These events detail common adversary
behaviors and techniques, targeted industries, and observed software and accompanying
privilege levels. With this data, defenders can develop a threat-informed defense
strategy focused on the top techniques observed in the wild and the threats to their
organization based on location, industry sector, and deployed platforms.

Framing our Analysis
--------------------

While our volume of data has increased significantly, there are caveats to keep
in mind when reading our results. Primarily, we are limited to the data we were
provided. While getting the data straight from vendors is beneficial, it
introduces biases. To ameliorate this bias, we have a diverse set of providers
and a large data set, which reduces some skewing within the data. 

Additionally, the quality of the data is limited to what the vendors generate. We
provide a data model for submitting data, but it is up to the vendors which fields to
submit to us. While some fields are required, such as technique and data source; others
are optional, such as region or privilege level. We also trust our contributors
to provide complete and accurate data. Mapping observed events to adversary techniques
is an art form and therefore has some degree of subjectivity. Where an adversary is
using PowerShell to run an executable with a valid account, one analyst may mark the
event as PowerShell Scripting, while another might mark it as Valid Accounts; it depends
on the context and the analyst's perspective. One mitigation for this bias is to mark the
data with all relevant techniques (both PowerShell and Valid Accounts).

Most of the events in our dataset are machine-generated and are not manually validated.
This means that the labelling for those events is dependent on the tools and
configurations used by the vendor. This can lead to a significant number of false
positives or false negatives, potentially skewing our data in unknown ways.

Our data is based on events that were found, not necessarily all attacks that occurred.
Therefore, the shifts in techniques that occur over time may more accurately reflect the
community’s ability to detect certain techniques, rather than those techniques being
used more frequently. Despite these limitations, our data still gives us a unique
insight into common techniques occurring in the wild.

Due to our time range (26 months) and variances in the ATT&CK version used by
contributors, the Sightings we receive are sometimes notated in older versions of
ATT&CK. As the ATT&CK knowledgebase evolves, techniques are added, removed, or merged.
This causes issues when interpreting our data. For example, Timestomp was in our top 15
techniques. However, it has since been merged into Indicator Removal. This presents a
challenge for us as we normalize the data and for the readers, who may be using
different versions of ATT&CK. We have done our best to normalize all techniques to the
current version of ATT&CK (V14) for consistency.
