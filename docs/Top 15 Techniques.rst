Top 15 Techniques
##################

The following is a more in-depth review of the top 15 most observed techniques. If a technique has sub-techniques in the ATT&CK framework, then we divided it into its sub-techniques; however, we only focused on the sub-techniques seen in our data. This provides more granular glimpse into each technique for defenders. The majority of the top 15 techniques abuse legitimate system tools. This underscores the idea that adversaries are attempting to appear as legitimate users. 
We have incorporated prevention methods from the `Center’s mappings <https://mitre-engenuity.org/cybersecurity/center-for-threat-informed-defense/our-work/nist-800-53-control-mappings/>`_ of ATT&CK to the `NIST SP 800-53 <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf/>`_ and detection methods from the `Cyber Analytics Repository <https://car.mitre.org/analytics/>`_ and the Center’s `Sensor Mappings for ATT&CK <https://mitre-engenuity.org/cybersecurity/center-for-threat-informed-defense/our-work/sensor-mappings-to-attack/>`_, which connects conceptual data sources to sensors and other tools . Due to the number of Windows events in our data, we chose to focus on sensor mappings for Sysmon and Windows event logs (WinEvtx). Overall, several prevention and detection controls focused on creating strong baselines, restricting permissions, and refining logs for process creation to detect and disrupt adversary behaviors.

1. Command and Scripting Interpreter `[T1059] <https://attack.mitre.org/techniques/T1059/>`_
***********************************************
Description
-----------
.. figure:: _static/T1059_attempt.png
   :alt: Breakdown of T1059. 
   :scale: 20%
   :align: right

Command and Scripting Interpreter is a commonly used living-off-the-land technique. Most platforms have built-in command-line interfaces or scripting capabilities, allowing adversaries to use them for executing arbitrary commands, scripts, or binaries.

Overall, T1059 was the most sighted technique in our data, in part because we normalized our data, which included T1064 and T1086 from previous ATT&CK versions, to T1059. The overwhelming majority of the sightings came from PowerShell `(T1059.001) <https://attack.mitre.org/techniques/T1059/001/>`_. This is not surprising as it is a common tool used by adversaries for its ubiquity, versatility, and ability to obfuscate activity. The second most observed sub-technique the Windows Command Shell `(T1059.003) <https://attack.mitre.org/techniques/T1059/003/>`_, which is similarly unsurprising for its ubiquity in Windows environments. The remaining sub-techniques make up less than 5%: 

* Visual Basic `(T1059.005) <https://attack.mitre.org/techniques/T1059/005/>`_ 
* Unix Shell `(T1059.004) <https://attack.mitre.org/techniques/T1059/004/>`_ 
* Python `(T1059.006) <https://attack.mitre.org/techniques/T1059/006/>`_ 
* JavaScript `(T1059.007) <https://attack.mitre.org/techniques/T1059/007/>`_
* AppleScript `(T1059.002) <https://attack.mitre.org/techniques/T1059/002/>`_ 

While these techniques are not difficult to monitor for, they are regularly used by benign programs, which could cause false positives for defenders to investigate. 

T1059 was evenly distributed between user and SYSTEM level privileges. It followed the overall data trends, with the US as the top region, Windows as the top platform, Manufacturing as the top sector, and Heodo (another name for Emotet) as the top software.

Prevention
----------
NIST lists 24 security controls to mitigate Command and Script Interpreter:

* AC-2 Account Management (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* AC-3 Access Enforcement (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* AC-5 Separation of Duties (Also mitigates PowerShell)
* AC-6 Least Privilege (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* AC-17 Remote Access (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* CA-7 Continuous Monitoring (Also mitigates Visual Basic and JavaScript)
* CA-8 Penetration Testing 
* CM-2 Baseline Configuration (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* CM-5 Access Restrictions for Change (Also mitigates PowerShell and Python)
* CM-6 Configuration Settings (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* CM-7 Least Functionality (Also mitigates Visual Basic and JavaScript)
* CM-8 System Component Inventory (Also mitigates PowerShell, Visual Basic, JavaScript)
* CM-11 User-Installed Software (Also mitigates Python)
* IA -2 Identification and Authentication (organizational Users) (Also mitigates PowerShell)
* IA-8 Identification and Authentication (non-organizational Users) (Also mitigates PowerShell)
* IA-9 Service Identification and Authentication (Also mitigates PowerShell and AppleScript)
* RA-5 Vulnerability Monitoring and Scanning (Also mitigates PowerShell, Visual Basic, and JavaScript)
* SC-18 Mobile Code (Also mitigates Visual Basic and JavaScript)
* SI-2 Flaw Remediation (Also mitigates PowerShell, Visual Basic, Python)
* SI-3 Malicious Code Protection (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* SI-4 System Monitoring (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* SI-7 Software, Firmware, and Information Integrity (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* SI-10 Information Input Validation (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)
* SI-16 Memory Protection (Also mitigates PowerShell, AppleScript, Visual Basic, Windows Command Shell, Unix Shell, Python, JavaScript)

NIST lists 1 security controls to mitigate Python:

* CM-3 Configuration Change Control

NIST lists 4 security controls to mitigate AppleScript:

* SR-4 Provenance
* SR-5 Acquisition Strategies, Tools, and Methods
* SR-6 Supplier Assessments and Reviews
* SR-11 Component Authenticity

Detections
----------
CAR 
^^^
Rules for the core technique: 

* `CAR-2021-01-002: Unusually Long Command Line Strings <https://car.mitre.org/analytics/CAR-2021-01-002/>`_ 

Rules for PowerShell: 

* `CAR-2014-04-003: PowerShell Execution <hhttps://car.mitre.org/analytics/CAR-2014-04-003/>`_ 
* `CAR-2014-11-004: Remote PowerShell Sessions <https://car.mitre.org/analytics/CAR-2014-11-004/>`_ 

Rules for Windows Command Shell:

* `CAR-2013-02-003: Processes Spawning cmd.exe <https://car.mitre.org/analytics/CAR-2013-02-003/>`_
* `CAR-2014-11-002: Outlier Parents of Cmd <https://car.mitre.org/analytics/CAR-2014-11-002/>`_

Rules for Visual Basic:

* `CAR-2013-04-002: Quick execution of a series of suspicious commands <https://car.mitre.org/analytics/CAR-2013-04-002/>`_

Sensor Mappings for ATT&CK 
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
  :widths: 30 30
  :header-rows: 0

  * - Sysmon
    - 1, 7, 30 

  * - Winevtx
    - 4103, 4104, 4688, 4696 
