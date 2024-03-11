Lessons Learned
===============

We discovered multiple issues during analysis. One of the most significant issues was
the different ATT&CK versions present in our data. While ATT&CK updates occur twice per
year, often they are minor updates. However, our data spans 28 months and includes data
from older ATT&CK versions, such as ATT&CK version 7 which introduced many new
techniques and depreciated/revoked several others. While this was released in 2020, we
still found data using old Technique IDs pre-version 7. As a short-term solution, we
used specific queries in ELK or wrote our own python scripts to generate correct
visualizations and statistics. However, this proved extremely time-consuming. In future
versions of the Sightings Ecosystem, we would limit which versions of ATT&CK that
contributions could contain. By requiring data to be in ATT&CK version 12 and up, for
example, we can mitigate how much normalization is required to have all data aligned
with the most current version of ATT&CK.

While our data model includes many interesting fields, their lack of reporting resulted
in analysis that was not completely representative and had to be heavily caveated.
Optional fields, such as software_name, were reported in only a small sub-set of our
data. In many cases, privilege_level and sector, though required fields, contained
nondescript answers, such as none and unknown, respectively. This severely reduced the
amount of data that contained descriptive answers in these fields, resulting in analysis
that tended to cover only a third of our data. For future versions of the Sightings
Ecosystem, we would strongly encourage all fields to be included and contain descriptive
information. This allows us to provide additional and more detailed analysis to the
public regarding some interesting fields, such as privilege levels and software used in
the wild.

While we improved our methods and infrastructure to ingest and analyze data, we still
encountered several issues. We had many instances where wiping and re-ingesting the data
into Elastic was required to fix different issues. In some cases, the ingest process
would stall due to our large data set, adding additional time to our troubleshooting.
While mitigating data discrepancies, we exported the data for analysis. However, this
was also time-consuming due to our large data set. Since we expect our data set to
continue to grow, it will be crucial to identify better ways to ingest and analyze the
data.
