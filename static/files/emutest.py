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

