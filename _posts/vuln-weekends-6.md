Vulnerable Weekends #6: WPS Bruteforce and CoCSoft Stream Down
==============================================================
date: 01/Jan/2012
summary: This is a report on recent security advisories published for WPS Bruteforce and CoCSoft Stream Down.
tags: vulnweekends

## Introduction
Report #6A analyzes the WPS implementation flaw that allows brute force guessing of the 8 digit PIN used to restrict wireless access to authenticated users.

Report #6B analyzes the memory corruption vulnerability in the CoCSoft Stream Down that could allow execution of arbitrary code on the targeted system.

## Vulnerability Report #6A: Multiple WPS Implementations Brute Force Authentication Bypass Vulnerability

**Vulnerable Product**: Installations of WPS enabled wireless devices

**CVE ID**: [CVE-2011-5053](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-5053)

**CVSS v2 Score**:  
**Access Vector**: NETWORK  
**Access Complexity**: MEDIUM  
**Authentication**: NONE  

**Confidentiality Impact**: COMPLETE  
**Integrity Impact**: COMPLETE  
**Availability Impact**: COMPLETE  
**Base Score**: 9.3  

**Exploitability**: FUNCTIONAL  
**Remediation Level**: WORKAROUND  
**Report Confidence**: CONFIRMED  
**Temporal Score**: 8.4  

### Details
Multiple WiFi Protected Setup (WPS) implementations were reported to contain a vulnerability that could be leveraged to bypass authentication checks and gain privileged access to the targeted wireless devices. The vulnerability has been identified within the WPS specification and it enables brute force detection of the PIN used to authenticate a remote wireless user.

The vulnerability exists because the WPS specification allows a remote attacker to guess the 8 digit PIN being used to authenticate remote wireless users. The first 4 digits of this PIN could be guessed by attempting multiple connections to the wireless AP with incorrect PIN values and analyzing the received `EAP-NACK` responses.

The `EAP-NACK` messages provide information that could be leveraged to successfully calculate the first and second halves of the 8 digit PIN being used. The number of brute force attempts to guess the PIN is also reduced because the 8th digit of this PIN is always a checksum which can be easily derived. This analysis brings the total number of brute force attempts to be 104 + 103; i.e 11,000 attempts to successfully calculate the WPS PIN for the targeted AP.

Since most vendors, except for Netgear, do not implement a lock down functionality for blocking such brute force attempts, the time complexity to successfully execute this attack is reduced significantly. On some implementation the overhead of processing such rapid surge of authentication requests leads to an internal state corruption, which could only be recovered via a device reboot. This makes it possible to launch denial of service (DoS) attacks on the targeted AP.

### Vulnerability Sources
[bid:51187](http://www.securityfocus.com/bid/51187)  
[sviehb.wordpress.com](http://sviehb.wordpress.com/2011/12/27/wi-fi-protected-setup-pin-brute-force-vulnerability/)  

## Vulnerability Report #6B: CoCSoft Sream Down Insufficient Boundary Checks Buffer Overflow Vulnerability

**Vulnerable Product**: Installations of CoCSoft Stream Down with versions 6.8 and prior

**CVE ID**: [CVE-2011-5052](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-5052)

**CVSS v2 Score**:  
**Access Vector**: NETWORK  
**Access Complexity**: LOW  
**Authentication**: NONE  

**Confidentiality Impact**: PARTIAL  
**Integrity Impact**: PARTIAL  
**Availability Impact**: PARTIAL  
**Base Score**: 7.5  

**Exploitability**: FUNCTIONAL  
**Remediation Level**: UNAVAILABLE  
**Report Confidence**: UNCORROBORATED  
**Temporal Score**: 6.8  

### Details
CoCSoft Stream Down media download application is prone to a buffer overflow vulnerability that could be leveraged to execute remote code or to cause a denial of service condition on the targeted system.

The vulnerable application fails to impose sufficient size limits on user-supplied input before copying it to a fixed length destination buffer. This implementation flaw could allow injection of arbitrary shellcode into the targeted system's memory space, leading to a memory corruption error. Later execution of this shellcode could allow the attacker to launch additional attacks on the targeted system.

CoCSoft has not yet confirmed this vulnerability. Users are advised to immediately stop using the vulnerable application.

### Vulnerability Sources
[bid:51190](http://www.securityfocus.com/bid/51190/)  

### Generic Sources
[cve.mitre.org](http://cve.mitre.org)  
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)  
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)  
