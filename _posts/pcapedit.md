pcapedit: An Interactive Scapy-based Pcap Editor
================================================
date: 15/Nov/2014
summary: pcapedit is an interactive pcap editor. It provides quick shorthand over Scapy commands and aims to be useful for mundane pcap editing tasks. The interactive mode allows saving of command history to a script which can then be used to edit multiple files together.
tags: code

## Introduction

While working with pcap files, I occasionally come across situations where I need to edit them for some weird usecases. When in such a situation, I had to write a loop that iterates over packets, check if the current packet needs modification, apply changes if so and save these changes to a new pcap. As I repeated these steps a few times, need for automation became obvious. I sat together with my colleague and good friend [Natraj](http://x00itachi.blogspot.in/) and discussed about how we can automate this process so that it helps with our IPS signature development efforts. Eventually, a draft for an interactive tool was formulated and [pcapedit](https://github.com/7h3rAm/pcapedit) was born.

`pcapedit` is a Python-based tool that allows users to enter commands to edit and save pcaps. It has a hard dependency on `Scapy` and `cmd2` modules so make sure these are installed. Here is a snippet from test run:

```
$ ./pcapedit.py
PcapEdit - An Interactive Pcap Editor

>>>
>>>
>>> help

Documented commands (type help <topic>):
========================================
_load           commands  history  ls       r         shell
_relative_load  ed        l        outpcap  run       shortcuts
analyze         edit      li       pause    save      show
back            hexdump   list     pdfdump  Scapycmd  summary
cmdenvironment  hi        load     py       set       wireshark

Undocumented commands:
======================
EOF  eof  exit  help  q  quit

>>> commands

  [01] analyze ......... load a pcap for analysis
  [02] ls .............. list packet details
  [03] summary ......... show summary of a packet
  [04] hexdump ......... show hexdump of a packet
  [05] pdfdump ......... dump packet to a PDF
  [06] Scapycmd ........ show Scapy command to generate a packet
  [07] wireshark ....... show a packet in Wireshark
  [08] edit ............ select a packet for set operations
  [09] outpcap ......... set name for output pcap
  [10] set ............. change value of a protocol field
  [11] save ............ save packets to a pcap

>>> q
```

## Usecases

So we have a few commands to try out. Let's assume that you have a `http.pcap` file that needs editing. Let's see how pcapedit can be useful in this case:

```
$ ./pcapedit.py
PcapEdit - An Interactive Pcap Editor

>>> analyze http.cap
Read 43 packets from http.cap
(http.cap) >>> summary
     0: 2004/05/13 15:47:07    145.254.160.237:3372 -> 65.208.228.223:80       TCP S
     1: 2004/05/13 15:47:08       65.208.228.223:80 -> 145.254.160.237:3372    TCP SA
     2: 2004/05/13 15:47:08    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
     3: 2004/05/13 15:47:08    145.254.160.237:3372 -> 65.208.228.223:80       TCP PA (479 bytes)
     4: 2004/05/13 15:47:08       65.208.228.223:80 -> 145.254.160.237:3372    TCP A
     5: 2004/05/13 15:47:08       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
     6: 2004/05/13 15:47:09    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
     7: 2004/05/13 15:47:09       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
     8: 2004/05/13 15:47:09    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
     9: 2004/05/13 15:47:09       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    10: 2004/05/13 15:47:09       65.208.228.223:80 -> 145.254.160.237:3372    TCP PA (1380 bytes)
    11: 2004/05/13 15:47:09    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    12: 2004/05/13 15:47:09    145.254.160.237:3009 -> 145.253.2.203:53        UDP (47 bytes)
    13: 2004/05/13 15:47:09       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    14: 2004/05/13 15:47:10    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    15: 2004/05/13 15:47:10       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    16: 2004/05/13 15:47:10        145.253.2.203:53 -> 145.254.160.237:3009    UDP (244 bytes)
    17: 2004/05/13 15:47:10    145.254.160.237:3371 -> 216.239.59.99:80        TCP PA (721 bytes)
    18: 2004/05/13 15:47:10    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    19: 2004/05/13 15:47:10       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    20: 2004/05/13 15:47:10       65.208.228.223:80 -> 145.254.160.237:3372    TCP PA (1380 bytes)
    21: 2004/05/13 15:47:10    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    22: 2004/05/13 15:47:10       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    23: 2004/05/13 15:47:10        216.239.59.99:80 -> 145.254.160.237:3371    TCP A
    24: 2004/05/13 15:47:11    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    25: 2004/05/13 15:47:11        216.239.59.99:80 -> 145.254.160.237:3371    TCP PA (1430 bytes)
    26: 2004/05/13 15:47:11        216.239.59.99:80 -> 145.254.160.237:3371    TCP PA (160 bytes)
    27: 2004/05/13 15:47:11    145.254.160.237:3371 -> 216.239.59.99:80        TCP A
    28: 2004/05/13 15:47:11       65.208.228.223:80 -> 145.254.160.237:3372    TCP PA (1380 bytes)
    29: 2004/05/13 15:47:11    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    30: 2004/05/13 15:47:11       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    31: 2004/05/13 15:47:11       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    32: 2004/05/13 15:47:11    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    33: 2004/05/13 15:47:11       65.208.228.223:80 -> 145.254.160.237:3372    TCP A (1380 bytes)
    34: 2004/05/13 15:47:11    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    35: 2004/05/13 15:47:12        216.239.59.99:80 -> 145.254.160.237:3371    TCP PA (1430 bytes)
    36: 2004/05/13 15:47:12    145.254.160.237:3371 -> 216.239.59.99:80        TCP A
    37: 2004/05/13 15:47:12       65.208.228.223:80 -> 145.254.160.237:3372    TCP PA (424 bytes)
    38: 2004/05/13 15:47:12    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    39: 2004/05/13 15:47:25       65.208.228.223:80 -> 145.254.160.237:3372    TCP FA
    40: 2004/05/13 15:47:25    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
    41: 2004/05/13 15:47:37    145.254.160.237:3372 -> 65.208.228.223:80       TCP FA
    42: 2004/05/13 15:47:37       65.208.228.223:80 -> 145.254.160.237:3372    TCP A
(http.cap) >>>
(http.cap) >>> summary 6
     6: 2004/05/13 15:47:09    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
(http.cap) >>>
```

The `summary` command displays a listing of all packets and their most common attributes. When provided an integer argument, it considers that to be the packet index and shows a one-line description for the packet itself. Let's now assume you need to edit packet #6:

```
(http.cap) >>> edit 6
Editing packet id: 6
     6: 2004/05/13 15:47:09    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
(http.cap|#6) >>>
(http.cap|#6) >>> set ether.src 11:22:33:44:55
     6: Ether.src: 00:00:01:00:00:00 -> 11:22:33:44:55
(http.cap|#6) >>>
(http.cap|#6) >>> set ether.dst 55:44:33:22:11
     6: Ether.dst: fe:ff:20:00:01:00 -> 55:44:33:22:11
(http.cap|#6) >>>
(http.cap|#6) >>> set ether.type 2048
     6: Ether.type: 2048 -> 2048
(http.cap|#6) >>>
(http.cap|#6) >>> set tcp.sport 1234
     6: TCP.sport: 3372 -> 1234
(http.cap|#6) >>>
(http.cap|#6) >>> set tcp.dport 4321
     6: TCP.dport: 80 -> 4321
(http.cap|#6) >>>
(http.cap|#6) >>> ls
dst        : DestMACField         = '55:44:33:22:11' (None)
src        : SourceMACField       = '11:22:33:44:55' (None)
type       : XShortEnumField      = 2048            (0)
--
version    : BitField             = 4L              (4)
ihl        : BitField             = 5L              (None)
tos        : XByteField           = 0               (0)
len        : ShortField           = 40              (None)
id         : ShortField           = 3910            (1)
flags      : FlagsField           = 2L              (0)
frag       : BitField             = 0L              (0)
ttl        : ByteField            = 128             (64)
proto      : ByteEnumField        = 6               (0)
chksum     : XShortField          = None            (None)
src        : Emph                 = '145.254.160.237' (None)
dst        : Emph                 = '65.208.228.223' ('127.0.0.1')
options    : PacketListField      = []              ([])
--
sport      : ShortEnumField       = 3372            (20)
dport      : ShortEnumField       = 4321            (80)
seq        : IntField             = 951058419       (0)
ack        : IntField             = 290219760       (0)
dataofs    : BitField             = 5L              (None)
reserved   : BitField             = 0L              (0)
flags      : FlagsField           = 16L             (2)
window     : ShortField           = 9660            (8192)
chksum     : XShortField          = None            (None)
urgptr     : ShortField           = 0               (0)
options    : TCPOptionsField      = {}              ({})
None
(http.cap|#6) >>>
```

So we selected the packet id, provided the respective protocol field names, new values and used the `ls` command to glance over changes. Since all looks good, we can now request `pcapedit` to save these changes, which it will then write to a `filename.mod.pcap` named file (you can override the default name and provide new name via the `outpcap` command):

```
(http.cap|#6) >>> save
Wrote 1 packet(s) to http.mod.cap
(http.cap|#6) >>>
(http.cap|#6) >>> q
$
$ ls -l *.cap
-rwxrwxr-x 1 shiv shiv 25803 Nov 15 12:22 http.cap
-rw-rw-r-- 1 shiv shiv    94 Nov 15 14:31 http.mod.cap
```

One thing to note here is that the `save` command only write one packet (#6) to the file and skip the rest. This is because `pcapedit` is a context-sensitive tool, ie. `it takes current context into consideration while executing commands`. Since at the time of issuing `save` command, the user was in per-packet editing mode (for packet #6), it intentionally skipped other packets. This is an immensely powerful feature as packets can now be edited individually and extracted from source pcap file to a new pcap file. However, if one wishes to save all packets, all they have to do is issue the `back` command to exit per-packet editing mode and then issue `save` command which will now honor the context and work as expected:

```
(http.cap|#6) >>> back
(http.cap) >>>
(http.cap) >>> save
Wrote 43 packet(s) to http.mod.cap
(http.cap) >>> q
$
$ ls -l *.cap
-rw-rw-r-- 1 shiv shiv 25803 Nov 15 12:22 http.cap
-rw-rw-r-- 1 shiv shiv 25901 Nov 15 14:09 http.mod.cap
```

Here's a screenshot of Wireshark parsing and decoding the edited packet:

![pcapedit-wireshark.png](/static/files/posts_pcapedit/pcapedit-wireshark.png.webp)

So at this point we know how to edit individual packets and save them to a new file, but doing this for hundreds or thousands of packets would still remain a daunting task and something that needs automation. That's where the *scriptfile* feature comes handy. You can save commands to a file and pass them as input to `pcapedit` and it will happily do as instructed:

```
$ ./pcapedit.py <tcpcmdstest.txt
PcapEdit - An Interactive Pcap Editor

>>> Read 43 packets from http.cap
(http.cap) >>>
(http.cap) >>> Editing packet id: 6
     6: 2004/05/13 15:47:09    145.254.160.237:3372 -> 65.208.228.223:80       TCP A
(http.cap|#6) >>>
(http.cap|#6) >>>      6: Ether.src: 00:00:01:00:00:00 -> 11:22:33:44:55
(http.cap|#6) >>>      6: Ether.dst: fe:ff:20:00:01:00 -> 55:44:33:22:11
(http.cap|#6) >>>      6: Ether.type: 2048 -> 2048
(http.cap|#6) >>>
(http.cap|#6) >>>      6: IP.version: 4 -> 88
(http.cap|#6) >>>      6: IP.ihl: 5 -> 56
(http.cap|#6) >>>      6: IP.tos: 0 -> 33
(http.cap|#6) >>>      6: IP.len: 40 -> 36
(http.cap|#6) >>>      6: IP.id: 3910 -> 12
(http.cap|#6) >>>      6: IP.flags: 2 -> 81
(http.cap|#6) >>>      6: IP.frag: 0 -> 22
(http.cap|#6) >>>      6: IP.ttl: 128 -> 27
(http.cap|#6) >>>      6: IP.proto: 6 -> 15
(http.cap|#6) >>>      6: IP.chksum: None -> 78
(http.cap|#6) >>>      6: IP.src: 145.254.160.237 -> 12
(http.cap|#6) >>>      6: IP.dst: 65.208.228.223 -> 21
(http.cap|#6) >>>      6: IP.options: [] -> ['99']
(http.cap|#6) >>>
(http.cap|#6) >>>      6: TCP.sport: 3372 -> 1234
(http.cap|#6) >>>      6: TCP.dport: 80 -> 4321
(http.cap|#6) >>>      6: TCP.seq: 951058419 -> 11
(http.cap|#6) >>>      6: TCP.ack: 290219760 -> 12
(http.cap|#6) >>>      6: TCP.dataofs: 5 -> 1
(http.cap|#6) >>>      6: TCP.reserved: 0 -> 9
(http.cap|#6) >>>      6: TCP.flags: 16 -> 90
(http.cap|#6) >>>      6: TCP.window: 9660 -> 36
(http.cap|#6) >>>      6: TCP.chksum: None -> 88
(http.cap|#6) >>>      6: TCP.urgptr: 0 -> 67
(http.cap|#6) >>>      6: TCP.options: {} -> {}
(http.cap|#6) >>>
(http.cap|#6) >>>      6: 2004/05/13 15:47:09                 12:1234 -> 21:4321                 TCP SPAE
(http.cap|#6) >>>
(http.cap|#6) >>> Wrote 11 packet(s) to http.mod.cap
(http.cap|#6) >>>
(http.cap|#6) >>> q
$
$ ls -l *.cap
-rwxrwxr-x 1 shiv shiv 25803 Nov 15 12:22 http.cap
-rw-rw-r-- 1 shiv shiv  6805 Nov 15 14:44 http.mod.cap
$
```

## Conclusion

There are a few other nifty commands that will be useful and I strongly recommend you to give `pcapedit` a try.
