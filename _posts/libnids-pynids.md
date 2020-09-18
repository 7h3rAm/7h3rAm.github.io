Network Stream Reassembly and Defragmentation
=============================================
date: 18/Jun/2013
summary: Libnids is a library that emulates Linux kernel 2.0.x TCP/IP stack to offer IP defragmentation, TCP reassembly and port scan detection features. This post talks about the Python wrapper and how to use it.
tags: code

## Introduction

[Libnids](http://libnids.sourceforge.net/) is a library that emulates Linux kernel 2.0.x TCP/IP stack to offer IP defragmentation, TCP reassembly and port scan detection features. It allows programs to accept arbitrary packet data, either from a packet capture file or directly from a network interface and extract TCP streams out of it. This stream is what layer 7 applications will process and as such it is a very good source for inspection tools to look for malicious content in it. In this post, we'll be seeing how Libnids and its Python binding can be used to create a nifty network inspection utility.

## Installation and Testing

We'll be using the [pynids](https://jon.oberheide.org/pynids/) Python binding from [Jon Oberheide](https://jon.oberheide.org/). Installation instructions are very well documented within the `README` file and I suggest you read and follow them. Let's have a look at an example program to test pynids installation:

```python
#!/usr/bin/env python

import sys
import nids

end_states = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)

def tcpcallback(tcp):
    if tcp.nids_state == nids.NIDS_JUST_EST:
        ((src, sport), (dst, dport)) = tcp.addr
        tcp.client.collect = 1
        tcp.server.collect = 1

    elif tcp.nids_state == nids.NIDS_DATA:
        tcp.discard(0)

    elif tcp.nids_state in end_states:
        ((src, sport), (dst, dport)) = tcp.addr
        print "[+] %s:%s - %s:%s (CTS: %dB | STC: %dB)" % (src, sport, dst, dport,
                len(tcp.server.data[:tcp.server.count]),
                len(tcp.client.data[:tcp.client.count]))

def main():
    if len(sys.argv) == 2:
        nids.param("filename", sys.argv[1])

    nids.init()
    nids.register_tcp(tcpcallback)

    try:
        nids.run()
    except nids.error, e:
        print "[-] Error: %s" % (e)
    except Exception, e:
        print "[-] Exception: %s" % (e)

if __name__ == '__main__':
    main()
```

Above program initializes Libnids and registers a TCP callback that would be called for each TCP packet seen by the library. For each new connection, the callback function requests Libnids to collect both client-to-server (CTS) and server-to-client (STC) flowing traffic. When the connection is closed/terminated/timed out, the above program dumps total bytes of data seen on both directions for the closed stream:

```
$ python nidstest.py ~/toolbox/testfiles/pcaps/http_witp_jpegs.cap
[+] 10.1.1.101:3177 - 10.1.1.1:80 (CTS: 476B | STC: 435B)
[+] 10.1.1.101:3188 - 10.1.1.1:80 (CTS: 574B | STC: 4601B)
[+] 10.1.1.101:3189 - 10.1.1.1:80 (CTS: 597B | STC: 8566B)
[+] 10.1.1.101:3190 - 10.1.1.1:80 (CTS: 600B | STC: 9330B)
[+] 10.1.1.101:3195 - 10.1.1.1:80 (CTS: 601B | STC: 692B)
[+] 10.1.1.101:3196 - 10.1.1.1:80 (CTS: 614B | STC: 1540B)
[+] 10.1.1.101:3197 - 10.1.1.1:80 (CTS: 622B | STC: 2509B)
[+] 10.1.1.101:3198 - 10.1.1.1:80 (CTS: 632B | STC: 9248B)
[+] 10.1.1.101:3199 - 10.1.1.1:80 (CTS: 632B | STC: 10990B)
[+] 10.1.1.101:3200 - 10.1.1.1:80 (CTS: 637B | STC: 191777B)
```

Let's have a look at the content of each stream and see what data will the TCP layer present as payload to application layer:

```
$ python nidsstream.py ~/toolbox/testfiles/pcaps/http.cap
[+] 145.254.160.237:3372 - 65.208.228.223:80 (CTS: 479B | STC: 18364B)

GET /download.html HTTP/1.1
Host: www.ethereal.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113
Accept: text/xml,application/xml,application/xhtml+xml,text/html
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Referer: http://www.ethereal.com/development.html


HTTP/1.1 200 OK
Date: Thu, 13 May 2004 10:17:12 GMT
Server: Apache
Last-Modified: Tue, 20 Apr 2004 13:17:00 GMT
ETag: "9a01a-4696-7e354b00"
Accept-Ranges: bytes
Content-Length: 18070
Keep-Alive: timeout=15, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=ISO-8859-1

<?xml version="1.0" encoding="UTF-8"?>
```

## Conclusion

The test pcap contains an HTTP session and the program dumps CTS and STC content (limited to first 300B) and this is exactly what the applications at layer 7 will send/receive while interacting with lower layers. Gaining direct access to this data opens up a number of possibilities for us to explore. Network inspection tools, primarily Intrusion Detection and Prevention Systems, will reassemble TCP packets and to create this buffer and then inspect this buffer in various ways to identify if it contains malicious content. One of the very common practices is to carry out signature based inspection on network streams to identify if they contain exploit traffic.

In an [upcoming post](/posts/20130915_libnids-python-ids.html), I'll try to explain how pynids and native Python modules can be used to develop a minimal IDS from scratch. Stay tuned.
