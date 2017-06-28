Vulnerable Weekends #3: Cisco WebEx Player and ISC DHCP
=======================================================
date: 10/Dec/2011
summary:
tags: vulnweekends

### Introduction
Report #3A analyzes the Cisco WebEx Player remote code execution vulnerability. The vendor states that a functional exploit for this vulnerability exists, however no public sources confirm its availability.

Report #3B analyzes the ISC DHCP denial of service vulnerability. Although, DHCP requests will only be received from local clients, attackers could also exploit this vulnerability from an adjacent network using a relay agent that comes bundled with the vulnerable product suite.

### Vulnerability Report #3A: Cisco WebEx Player WRF Files Processing Remote Code Execution Vulnerability

**Vulnerable Product**: Installations of Cisco WebEx Player with versions T26 prior to SP49 EP40 and T27 prior to SP28

**CVE ID**: [CVE-2011-3319](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-3319)

**CVSS v2 Score**:
**Access Vector**: NETWORK
**Access Complexity**: MEDIUM
**Authentication**: NONE

**Confidentiality Impact**: COMPLETE
**Integrity Impact**: COMPLETE
**Availability Impact**: COMPLETE
**Base Score**: 9.3

**Exploitability**: FUNCTIONAL
**Remediation Level**: OFFICIAL FIX
**Report Confidence**: CONFIRMED
**Temporal Score**: 7.7

**Details**:
Cisco WebEx Player is an application that helps to playback or edit WebEx meetings recording, WebEx Recording Format (WRF) files.

The vulnerable software fails to perform sufficient sanitization on user-supplied input received via a malicious `.wrf` file. A shared library, `atdl2006.dll`, has been identified as the source of this vulnerability. The vulnerable library uses an unsanitized, user-supplied size parameter to allocate a dynamic buffer via the `memcpy()` function. However, due to insufficient checks on this parameter, a heap-based buffer overflow could be triggered.

Attackers who can successfully lure a targeted user to open a malicious .wrf file or visit a crafted webpage, could exploit this vulnerability. Once exploited, the attacker could execute arbitrary code on the targeted system with the privileges of the user.

The vendor, Cisco, has confirmed this vulnerability and provided official fixes to mitigate it. Users are requested to refer to the vendor advisory for further details.

**Vulnerability Sources**:
[cisco:20111026](http://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20111026-webex)
[zdi:11-341](http://www.zerodayinitiative.com/advisories/ZDI-11-341/)
[bid:50373](http://www.securityfocus.com/bid/50373)

### Vulnerability Report #3B: ISC DHCP Incorrect Extended Regular Expressions Processing Denial of Service Vulnerability

**Vulnerable Product**: Installations of ISC DHCP server with versions prior to 4.2.3-P1 and 4.1-ESV-R4

**CVE ID**: [CVE-2011-4539](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-4539)

**CVSS v2 Score**:
**Access Vector**: ADJACENT NETWORK
**Access Complexity**: MEDIUM
**Authentication**: NONE

**Confidentiality Impact**: NONE
**Integrity Impact**: NONE
**Availability Impact**: PARTIAL
**Base Score**: 2.9

**Exploitability**: UNPROVEN
**Remediation Level**: OFFICIAL FIX
**Report Confidence**: CONFIRMED
**Temporal Score**: 2.1

**Details**:
Internet Systems Consortium (ISC) provides an open source, reference implementation for Dynamic Host Configuration Protocol (DHCP) which includes components such as a server, a client and a relay agent.

The vulnerability exists within the server component which is responsible for handling DHCP requests received from local clients or from adjacent clients via a relay agent.

The vulnerable component incorrectly evaluates an extended regular expression consisting of a comparison operator such as `~=` or `~~`. While processing a DHCP request, if such operators are encountered within its configuration file, dhcpd.conf, the vulnerable component could terminate abnormally, leading to a denial of service (DoS) condition.

The vulnerability, however, could only be triggered if the targeted server has been configured to parse extended regular expressions. As such, only those installations where an administrator has manually configured the vulnerable component to use such operators, are exposed to this vulnerability.

The vendor, ISC, has confirmed this vulnerability and released patches for its mitigation. Users are requested to refer to the vendor advisory for further details.

**Vulnerability Sources**:
[isc](https://www.isc.org/software/dhcp/advisories/cve-2011-4539)
[bid:50971](http://www.securityfocus.com/bid/50971)

**Generic Sources**:
[cve.mitre.org](http://cve.mitre.org)
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)
