Vulnerable Weekends #7: Iptools rcmd DoS
========================================
date: 07/Jan/2012
summary:
tags: vulnweekends

### Vulnerability Report #7: Iptools rcmd Denial of Service Vulnerability

**Vulnerable Product**: Installations of Iptools with version 0.1.4

**CVE ID**: NA

**CVSS v2 Score**:
**Access Vector**: NETWORK
**Access Complexity**: LOW
**Authentication**: NONE

**Confidentiality Impact**: NONE
**Integrity Impact**: NONE
**Availability Impact**: PARTIAL
**Base Score**: 5

**Exploitability**: PROOF-OF-CONCEPT
**Remediation Level**: WORKAROUND
**Report Confidence**: UNCORROBORATED
**Temporal Score**: 4.1

**Details**:
Iptools is a popular set of tiny TCP/IP utilities implemented as Perl scripts, that include a minimalist webserver, a remote command server on the lines of Telnet, a TFTP server/client, SNMP browser, etc. The toolset has been reported to be vulnerable to a denial of service (DoS) vulnerability, specifically within its remote command server script, `rcmd`.

The vulnerable utility receives user-supplied input through its listening port, TCP/23, which is then tested against a set of weak sanitization checks. This input is used as a placeholder for the `EXPR` parameter used by the internal `chdir` function which parses it as a filename reference. Since this parameter could reference a string of an unbounded length, the directory change operation could generate an untrappable exception. This flaw could make the vulnerable utility unstable, effectively terminating the Perl interpreter abnormally, leading to the DoS condition. The following code snippet depicts where the vulnerability could have been introduced within the `rcmd` script:

```python
chop($curdir=`cd`);
print NS "$curdir> ";
while (<NS>) {
  print "Client request : ";
    print;
  CASE: {
      /cd / && do { $dir=$'; $dir=~s/\015\012//; print $dir if $debug;
                    chdir "$dir" || print NS "Invalid directory\015\012"  ; last CASE; };
      /^(\b)*(.:)/ && do { $drive=$2; ; print "driver:[$drive]" if $debug;
                    chdir "$drive" || print NS "Invalid drive\015\012"  ; last CASE; };
```

An official confirmation and software updates are currently unavailable. Users are requested to avoid using the vulnerable utility until official fixes are released. For a workaround, users could consider introducing restrictive firewall policies that prohibit unnecessary access to the vulnerable script from an unauthorized source.

**Vulnerability Sources**:
[bid:51312](http://www.securityfocus.com/bid/51312/)
[iptools](http://iptools.sourceforge.net/iptools.html)

**Generic Sources**:
[cve.mitre.org](http://cve.mitre.org)
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)
