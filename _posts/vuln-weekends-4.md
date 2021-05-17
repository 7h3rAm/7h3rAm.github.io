Vulnerable Weekends #4: Windows True-Type Fonts and Windows DVR-MS
==================================================================
date: 18/Dec/2011
summary: This is a report on recent security advisories published for Windows True-Type Fonts and Windows DVR-MS.
tags: vulnweekends

## Introduction
Report #4A analyzes the Microsoft Windows True-Type fonts handling vulnerability that the W32.Duqu malware leverages to install itself on vulnerable systems. Once installed, it could then leverage its elevated privileges to execute arbitrary code.

Report #4B analyzes the Microsoft Windows DVR-MS media files processing vulnerability that could also be leveraged to execute arbitrary code on the targeted system.

## Vulnerability Report #4A: Microsoft Windows Kernel-Mode Drivers True-Type Font Handling Remote Code Execution Vulnerability

**Vulnerable Product**: Installations of Microsoft Windows XP, Server 2003, Vista, Server 2008, and 7

**CVE ID**: [CVE-2011-3402](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-3402)

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

### Details
Microsoft Windows has been reported to contain a vulnerability that could be leveraged to execute arbitrary code on the targeted system. The vulnerability has been reported within the Kernel-Mode driver, `Win32k.sys`, that provides rendering support for True-Type fonts.

The vulnerability is due to the fact that the vulnerable font processing engine fails to perform mandatory boundary checks on user-supplied input received via crafted True-Type fonts embedded within a Microsoft Office `.doc` file. An attacker who could convince a remote user to open a malicious `.doc` file, containing the specially crafted content, could exploit this vulnerability to cause a memory corruption error within kernel space. Further, the attacker could leverage such memory corruption errors to inject arbitrary shellcode within system memory and execute it with `SYSTEM` privileges on the targeted system.

Public [sources](http://www.symantec.com/connect/w32-duqu_status-updates_installer-zero-day-exploit) confirm that the [W32.Duqu](http://tools.cisco.com/security/center/viewAlert.x?alertId=24425) malware, assumed to be a variant of [W32/Stuxnet-B](http://tools.cisco.com/security/center/viewAlert.x?alertId=20915), leverages this vulnerability to infect targeted systems.

The vendor, Microsoft, has released a [security bulletin](http://technet.microsoft.com/en-us/security/bulletin/MS11-087) to confirm this vulnerability and provided official patches for its mitigation. Users are requested to keep their systems updated with the latest available patches.

### Vulnerability Sources
[bid:50462](http://www.securityfocus.com/bid/50462)  
[cisco:24500](http://tools.cisco.com/security/center/viewAlert.x?alertId=24500)  
[symc](http://www.symantec.com/security_response/writeup.jsp?docid=2011-101814-1119-99)  

## Vulnerability Report #4B: Microsoft Windows Media Player DVR-MS Files Processing Remote Code Execution Vulnerability

**Vulnerable Product**: Installations of Microsoft Windows XP, Vista, and 7

**CVE ID**: [CVE-2011-3401](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-3401)

**CVSS v2 Score**:  
**Access Vector**: NETWORK  
**Access Complexity**: MEDIUM  
**Authentication**: NONE  

**Confidentiality Impact**: COMPLETE  
**Integrity Impact**: COMPLETE  
**Availability Impact**: COMPLETE  
**Base Score**: 9.3  

**Exploitability**: UNPROVEN  
**Remediation Level**: OFFICIAL FIX  
**Report Confidence**: CONFIRMED  
**Temporal Score**: 6.9  

### Details
Microsoft Windows Media Player has been reported to contain a vulnerability that could be leveraged to execute arbitrary code on the targeted system. The vulnerability exists within the `encdec.dll` library used by the vulnerable platforms.

The vulnerability is introduced while the affected software tries to process Microsoft Digital Video Recording (DVR-MS) media files. The affected software fails to perform sufficient security checks on user-supplied input received via such files, leading to a memory corruption error within kernel space. An attacker who could convince a targeted user to open a malicious `.dvr-ms` file, could exploit this vulnerability and leverage the memory corruption error to execute arbitrary code with `SYSTEM` privileges.

The vendor, Microsoft, has released a [security bulletin](http://technet.microsoft.com/en-us/security/bulletin/MS11-092) to confirm this vulnerability and provided official patches for its mitigation. Users are requested to keep their systems updated with the latest available patches.

### Vulnerability Sources
[bid:50957](http://www.securityfocus.com/bid/50957)  
[secunia:cve-2011-3401](http://secunia.com/advisories/cve_reference/CVE-2011-3401/)  

### Generic Sources
[cve.mitre.org](http://cve.mitre.org)  
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)  
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)  
