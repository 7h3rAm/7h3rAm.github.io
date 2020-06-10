Vulnerable Weekends #1: Mozilla and ProFTPd
===========================================
date: 20/Nov/2011
summary:
tags: vulnweekends

## Introduction
Last week Mozilla revised the major version number for its popular web browsing application, Firefox, taking it to version 8.0. Its been hardly a few days since Firefox 8.0 has been available publicly, reports about a denial of service (DoS) vulnerability within the latest and prior releases started to make news. I have tried to analyze this vulnerability and #1A is a report for the same.

The #1B report provides yet another interesting update related to a remote code execution (RCE) vulnerability confirmed within ProFTPd.

## Vulnerability Report #1A: Mozilla Firefox `OnStartRequest()` Function XPCOM Object Processing Denial of Service Vulnerability

**Vulnerable Product**: Installations of Mozilla Firefox with versions 8.0 and prior.

**CVE ID**: Not available

**CVSS v2 Score**:  
**Access Vector**: NETWORK  
**Access Complexity**: MEDIUM  
**Authentication**: NONE  

**Confidentiality Impact**: NONE  
**Integrity Impact**: NONE  
**Availability Impact**: PARTIAL  
**Base Score**: 4.3  

**Exploitability**: PROOF-OF-CONCEPT  
**Remediation Level**: UNAVAILABLE  
**Report Confidence**: UNCORROBORATED  
**Temporal Score**: 3.7  

### Details
Mozilla Firefox, the popular open source web browsing application, reportedly contains a vulnerability which could be leveraged by an attacker to cause a denial of service (DoS) condition on the targeted system.

The vulnerable web browser performs insufficient sanitization on user-supplied input encountered while processing crafted webpages.

Online reports indicate that the `OnStartRequest()` function which is defined within the `nsObjectLoadingContent.cpp` source file of the affected software is where the vulnerability resides. This function erroneously permits a comparison between a Cross Platform Common Object Model (XPCOM) object with a `NULL` value received as input. This flaw could return a `NS_BINDING_ABORTED` value to the calling function, leading to an abnormal termination of the vulnerable web browser.

An attacker who can successfully lure a targeted user to visit a malicious webpage that contains crafted input for the vulnerable function or who can persuade a user to open a malicious web page received as an e-mail attachment, could trigger this vulnerability. When the vulnerable web browser tries to process such crafted webpages, the above mentioned flaw is triggered, leading to the DoS condition on the targeted system.

Proof-of-concept (PoC) code to demonstrate the validity of the vulnerability claim and an impact of a successful exploit attempt has been made available on public sources like Exploit-DB.

The vendor, Mozilla, has not yet confirmed this vulnerability and as such there are no official patches or updates available for this vulnerability. Users are requested to get in touch with the vendor's support services to obtain updates for their installations.

### Vulnerability Sources
[xfdb:71288](http://xforce.iss.net/xforce/xfdb/71288)  
[bid:50667](http://www.securityfocus.com/bid/50667)  

## Vulnerability Report #1B: ProFTPd `pr_cmd_dispatch_phase()` Function Response Code Handling Arbitrary Code Execution Vulnerability

**Vulnerable Product**: Installations of ProFTPd versions with 1.3.3 and prior.

**CVE ID**: [CVE-2011-4130](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-4130)

**CVSS v2 Score**:  
**Access Vector**: NETWORK  
**Access Complexity**: LOW  
**Authentication**: SINGLE  

**Confidentiality Impact**: COMPLETE  
**Integrity Impact**: COMPLETE  
**Availability Impact**: COMPLETE  
**Base Score**: 9.0  

**Exploitability**: UNPROVEN  
**Remediation Level**: OFFICIAL FIX  
**Report Confidence**: CONFIRMED  
**Temporal Score**: 6.7  

### Details
ProFTPd, the popular FTP daemon, reportedly contains a vulnerability which could be leveraged by an attacker to execute arbitrary code on the targeted system.

The vulnerable daemon fails to manage a pool used for the client responses. While processing user requests, if an exceptional condition occurs, the daemon uses a response pointer to select user response to be sent for the triggered exception. However, due to a flaw within the code responsible for handling exceptions, the response pointer is incorrectly restored to the appropriate response code and it could be made to point to a desired memory location.

Online reports indicate that the `pr_cmd_dispatch_phase()` function defined within the main.c source file of the vulnerable daemon is where the vulnerability resides. The vulnerable function provides a mechanism for issuing calls to the registered ProFTPd modules. However, before entering the requested module, the daemon essentially stores the `resp_pool` state so that it can be used upon return. While the control is within the requested module, if an exception is triggered, the vulnerable daemon fails to restore `resp_pool` state, which could then be altered using a controlled memory corruption.

An attacker who can complete the initial authentication phase on the targeted system could successfully trigger this vulnerability. When the vulnerable daemon tries to handle an explicitly triggered exception, it could allow arbitrary code execution on the targeted system.

The vendor, ProFTPd.org, has confirmed this vulnerability and provided official updates to mitigate it. Users are requested to immediately apply the latest updates on their vulnerable installations.

### Vulnerability Sources
[zdi:11-328](http://www.zerodayinitiative.com/advisories/ZDI-11-328)  
[bid:50631](http://www.securityfocus.com/bid/50631)  

### Generic Sources
[cve.mitre.org](http://cve.mitre.org)  
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)  
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)  
