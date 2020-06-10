Vulnerable Weekends #5: MIT Kerberos and VLC TiVo
=================================================
date: 24/Dec/2011
summary:
tags: vulnweekends

## Introduction
Report #5A analyzes the MIT Kerberos Telnet remote, privileged code execution vulnerability. This vulnerability has been identified within the MIT Kerberos based Telnet installations that are provided with FreeBSD, GNU inetutils, etc.

Report #5B analyzes the VLC TiVo file parser arbitrary code execution vulnerability.

## Vulnerability Report #5A: MIT `krb5-appl` Telnet Client and Server `encrypt_keyid()` Remote Code Execution Vulnerability

**Vulnerable Product**: Installations of MIT krb5-appl derived telnet utilities prior to krb5-1.8

**CVE ID**: [CVE-2011-4862](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-4862)

**CVSS v2 Score**:  
**Access Vector**: NETWORK  
**Access Complexity**: LOW  
**Authentication**: NONE  

**Confidentiality Impact**: COMPLETE  
**Integrity Impact**: COMPLETE  
**Availability Impact**: COMPLETE  
**Base Score**: 10.0  

**Exploitability**: FUNCTIONAL  
**Remediation Level**: OFFICIAL FIX  
**Report Confidence**: CONFIRMED  
**Temporal Score**: 8.3  

### Details
MIT `krb5-appl` has been reported to contain a vulnerability that could be leveraged by a remote attacker to execute arbitrary code on the targeted system. The vulnerability has been reported in the code responsible for handling Kerberos based authentication mechanism.

The vulnerability was introduced when BSD telnet daemon and client utilities included support for cryptographic security via MIT Kerberos based authentication mechanism. This code was further included within FreeBSD and GNU inetutils making these vulnerable as well.

The vulnerability allows a pre-authentication memory corruption error that could be triggered remotely by submitting an arbitrarily long encryption key to the target system. Specifically, the vulnerability exists within the `encrypt_keyid()` function of the `encrypt.c` source file of the affected software:

```c
static void
encrypt_keyid(struct key_info *kp, unsigned char *keyid, int len)
{
   ...
    } else if ((len != kp->keylen) || (memcmp(keyid,kp->keyid,len) != 0)) {
    /*
     * Length or contents are different
     */
    kp->keylen = len;
    memcpy(kp->keyid,keyid, len);
    if (ep->keyid)
        (void)(*ep->keyid)(dir, kp->keyid, &kp->keylen);
    ...
}
```

The vulnerable source file defines the following structure to keep record of the encryption state:

```c
#define   MAXKEYLEN 64

static struct key_info {
    unsigned char keyid[MAXKEYLEN];
    int keylen;
    int dir;
    int *modep;
    Encryptions *(*getcrypt)();
} ki[2] = {
    { { 0 }, 0, DIR_ENCRYPT, &encrypt_mode, findencryption },
    { { 0 }, 0, DIR_DECRYPT, &decrypt_mode, finddecryption },
};
```

However, the vulnerable function fails to impose sufficient boundary restrictions on user-supplied encryption keys and copies those into `keyinfo` structure without honoring the `MAXKEYLEN` constant via a `memcpy` operation. This could cause a heap-based buffer overflow error, leading to the memory corruption error.

Successful exploitation could allow the attacker to leverage the memory corruption error to execute arbitrary code on the targeted system with the privileges of the affected software. Failed exploit attempts could result in a denial of service condition on the targeted system.

### Vulnerability Sources
[bid:51182](http://www.securityfocus.com/bid/51182)  
[kerberos:2011-008](http://web.mit.edu/kerberos/advisories/MITKRB5-SA-2011-008.txt)  
[freebsd:11-08](http://security.freebsd.org/advisories/FreeBSD-SA-11:08.telnetd.asc)  
[redhat:770325](https://bugzilla.redhat.com/show_bug.cgi?id=770325)  
[osvdb:78020](http://osvdb.org/78020)  

## Vulnerability Report #5B: VLC `.TY (TiVo)` File Parser Arbitrary Code Execution Vulnerability

**Vulnerable Product**: Installations of VLC Media Player with versions 0.9.0 through 1.1.12

**CVE ID**: NA

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
**Temporal Score**:6.9  

### Details
VLC Media Player has been reported to contain a vulnerability that could allow a remote attacker to execute arbitrary code on the targeted system. The vulnerability is introduced by the `libty_plugin` that helps parsing of `.ty` files.

```c
struct demux_sys_t
{
...
ty_rec_hdr_t    *rec_hdrs;          /* record headers array */
int             i_cur_rec;          /* current record in this chunk */
int             i_num_recs;         /* number of recs in this chunk */
...
};
```

The vulnerability exists due to an implementation flaw within the `get_chunk_header()` function of the `ty.c` source file of the vulnerable plugin. The vulnerable plugin improperly handles the record headers array, `rec_hdrs`, corrupting heap structures in the memory.

```c
diff --git a/modules/demux/ty.c b/modules/demux/ty.c
index e916b41..b181a6a 100644 (file)

--- a/modules/demux/ty.c
+++ b/modules/demux/ty.c
@@ -1887,6 +1887,7 @@ static int get_chunk_header(demux_t *p_demux)
     /*msg_Dbg( p_demux, "chunk has %d records", i_num_recs );*/

     free(p_sys->rec_hdrs);
+    p_sys->rec_hdrs = NULL;
     /* skip past the 4 bytes we "peeked" earlier */
     stream_Read( p_demux->s, NULL, 4 );
```

Successful exploitation could allow the attacker to leverage the memory corruption error further and execute arbitrary code on the targeted system within the security context of the affected software.

### Vulnerability Sources
[bid:51147](http://www.securityfocus.com/bid/51147)  
[vlc:sa1108](http://www.videolan.org/security/sa1108.html)  
[git.videolan.org](http://git.videolan.org/?p=vlc.git;a=blobdiff;f=modules/demux/)  

### Generic Sources
[cve.mitre.org](http://cve.mitre.org)  
[cvss-guide](http://www.first.org/cvss/cvss-guide.html)  
[cvss-calculator](http://nvd.nist.gov/cvss.cfm?calculator&adv&version=2)  
