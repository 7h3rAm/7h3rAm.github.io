Vulnerable Weekends #8: HP LoadRunner RCE
=========================================
date: 02/Jun/2012
summary: This is a report on recent security advisory published for HP LoadRunner RCE.
tags: vulnweekends

## Vulnerability Report #8: HP LoadRunner magentservice.exe Component Remote Code Execution Vulnerability

**Vulnerable Product**: Installations of HP LoadRunner prior to version 11 patch 4

**CVE ID**: [CVE-2011-4789](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-4789)

**CVSS v2 Score**:  
**Access Vector**: REMOTE  
**Access Complexity**: LOW  
**Authentication**: NONE  

**Confidentiality Impact**: COMPLETE  
**Integrity Impact**: COMPLETE  
**Availability Impact**: COMPLETE  
**Base Score**: 10  

**Exploitability**: FUNCTIONAL  
**Remediation Level**: OFFICIAL FIX  
**Report Confidence**: CONFIRMED  
**Temporal Score**: 8.3  

### Details
HP LoadRunner is vulnerable to a remote code execution vulnerability due to insufficient boundary checks performed on user-supplied input received via its `magentservice.exe` component.

The vulnerability exists due to an implementation flaw within the affected software. The vulnerable component listens for incoming requests on `23472/tcp` and it expects a size value within the first 32bits of user-supplied input. This value is used as-is, without any sanitization, for internal calculations that involve deriving the number of bytes to be copied in to a destination buffer. Due to the insufficient checks, a 32bit value of 0x00000000 could cause an error within the internal calculation logic and trigger a stack-based buffer overflow during a later copy operation. This action could allow a remote attacker to execute arbitrary code with `SYSTEM` privileges on the targeted system.

HP has confirmed this vulnerability and released a security patch for registered users.

### Vulnerability Sources
[bid:51398](http://www.securityfocus.com/bid/51398/)  
[hpsb:HPSBMU02785](https://h20565.www2.hp.com/portal/site/hpsc/public/kb/docDisplay?docId=emr_na-c03216705&ac.admitted=1338640006393.876444892.492883150)  
[metasploit](http://www.metasploit.com/modules/exploit/windows/misc/hp_magentservice)  
[zdi:12-016](http://www.zerodayinitiative.com/advisories/ZDI-12-016/)  

### Generic Sources
[cve.mitre.org](http://cve.mitre.org)  
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)  
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)  
