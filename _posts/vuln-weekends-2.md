Vulnerable Weekends #2: GNU GDB and Intel VT-d
==============================================
date: 03/Dec/2011
summary: This is a report on recent security advisories published for GNU GDB and Intel VT-d.
tags: vulnweekends

## Introduction
Report #2A analyzes the GNU GDB code execution vulnerability. Although online reports indicate that various vendors were aware of this vulnerability as early as April 2011 and are still involved in its resolution, there has been no official confirmation.

Report #2B provides an analysis for the acclaimed Intel VT-d chipsets privilege escalation vulnerability. Xen has confirmed this vulnerability and has released two patches that either disallow the virtual machine to boot if its using the vulnerable configuration or narrows down the scope of this vulnerability to a denial of service.

## Vulnerability Report #2A: GNU GDB Insecure Scripts Processing Arbitrary Code Execution Vulnerability

**Vulnerable Product**: Installations of GDB with versions 7.3.1 and prior.

**CVE ID**: [CVE-2011-4355](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-4355)

**CVSS V2 Score**:  
**Access Vector**: LOCAL  
**Access Complexity**: MEDIUM  
**Authentication**: SINGLE  

**Confidentiality Impact**: PARTIAL  
**Integrity Impact**: PARTIAL  
**Availability Impact**: PARTIAL  
**Base Score**: 4.1  

**Exploitability**: UNPROVEN  
**Remediation Level**: UNAVAILABLE  
**Report Confidence**: UNCORROBORATED  
**Temporal Score**: 3.3  

### Details
GDB, the GNU Project debugger, is one of the most valuable tools available for understanding the internals of a program. The debugger provides a wide array of options for its users to explore. One such option, however, could allow an authenticated attacker to execute arbitrary code on the targeted system.

The vulnerable debugger fails to perform sufficient sanitization on user-supplied input received via malicious Executable and Linkable Format (ELF) or Common Object File Format (COFF) files.

The vulnerable debugger looks for a special `.debug_gdb_scripts` section within such object files to obtain a list of scripts that are to be executed. The standard local file lookup procedure, which includes searching for the specified filename within the current directory and then through each of the file locations specified within the system path, is used to search for the specified script.

Since, the validity of such user-specified scripts is not taken into account before executing them, this feature could allow an attacker who has obtained privileged access to an enterprise system to execute arbitrary code. The attacker could install malicious scripts within the current directory or within one of the standard file search paths and then reference them using the vulnerable option from a crafted object file. When the vulnerable debugger initiates a debug operation on such object files, it could encounter the option and execute the requested scripts with the privileges of the user.

The vendor, GNU, has not yet confirmed this vulnerability and as such there are no official patches or updates available for this vulnerability. Users are requested to get in touch with the vendor to obtain patches/updates for their installations.

### Vulnerability Sources
[bid:50829](http://www.securityfocus.com/bid/50829)  
[redhat:703238](https://bugzilla.redhat.com/show_bug.cgi?id=703238)  

## Vulnerability Report #2B: Intel VT-d MSI Traps Injection Using PCI Passthrough Privilege Escalation Vulnerability

**Vulnerable Product**: Installations of Xen with versions 4.1.2 and prior.

**CVE ID**: [CVE-2011-1898](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-1898)

**CVSS V2 Score**:  
**Access Vector**: LOCAL  
**Access Complexity**: MEDIUM  
**Authentication**: SINGLE  

**Confidentiality Impact**: COMPLETE  
**Integrity Impact**: COMPLETE  
**Availability Impact**: COMPLETE  
**Base Score**: 6.6  

**Exploitability**: UNPROVEN  
**Remediation Level**: OFFICIAL FIX  
**Report Confidence**: CONFIRMED  
**Temporal Score**: 4.9  

### Details
Xen, a Virtual Machine Monitor (VMM), contains a vulnerability which an authenticated attacker could leverage to gain elevated privileges on the targeted system.

The vulnerable hypervisor fails to restrict a guest virtual machine, that has ownership of a PCI device, to edit the interrupt injection registers via Direct Memory Access (DMA) and trigger abrupt Message Signaled Interrupts (MSIs). This flaw could allow the attacker to inject arbitrary traps and gain privileged access on the host system.

Target platforms that support PCI passthrough to make certain PCI devices accessible within guest virtual machines and have the Interrupt Remapping feature either disabled or unsupported are exposed to this vulnerability.

An authenticated attacker who has sufficient privileges to execute a virtual machine, that has access to certain PCI devices, could exploit this vulnerability on the vulnerable platforms. Newer Intel chipsets include support for Interrupt Remapping and as such are immune to this vulnerability. However there is still a huge userbase for older, vulnerable hardware that makes this vulnerability critical.

The vendor, Xen, has confirmed this vulnerability and provided official patches to mitigate this vulnerability. Users are however informed that though official patches mitigate this vulnerability, the attacker could still cause a denial of service condition on the targeted system. The only available solution would be to either enable the `Interrupt Remapping` feature or upgrade to a hardware platform that supports it.

### Vulnerability Sources
[xen:00687](http://old-list-archives.xen.org/archives/html/xen-devel/2011-05/msg00687.html)  
[redhat:715555](https://bugzilla.redhat.com/show_bug.cgi?id=715555)  
[bid:48515](http://www.securityfocus.com/bid/48515)  

### Generic Sources
[cve.mitre.org](http://cve.mitre.org)  
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)  
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)  
