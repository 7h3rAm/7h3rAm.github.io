reverse-ex Challenge from Coursera's Malicious Software Course
==============================================================
date: 24/Aug/2013
summary: This is a writeup for an interesting challenge from recently concluded Malicious Software course on Coursera.
tags: ctf, reversing

## Introduction

The recently concluded [Malicious Software and its Undergound Economy](https://class.coursera.org/malsoftware-001/) course on [Coursera](https://www.coursera.org/) had an interesting reverse engineering challenge as part of its coursework: [reverse-ex](/static/files/posts_malsoftware_reverse_ex/reverse-ex). I found it interesting since it will be equally entertaining for someone who has never tried such challenges or one who has mastered many of them. This post details the steps I took to complete this challenge.

## Program Analysis and Testing

The first thing I normally do after obtaining such challenges is to test them with `file` command. This provides some insight about various file attributes like its type (ELF, PE, etc.), processor architecture compatibility, symbol table inclusion, etc:

```
$ file reverse-ex
reverse-ex: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[ sha1]=0x8dac70a14b40f115fc4a27041a3ae29227a55afb, not stripped
$
$ file -i reverse-ex
reverse-ex: application/x-executable; charset=binary
```

The above output tells us that this is a 32bit [ELF](http://en.wikipedia.org/wiki/Executable_and_Linkable_Format) binary, [dynamically linked](http://stackoverflow.com/questions/1993390/static-linking-vs-dynamic-linking), and has [symbols included](http://unix.stackexchange.com/questions/2969/what-are-stripped-and-not-stripped-executables-in-unix). This means that debugging and symbol resolution information has been preserved and packed inside the binary itself. This is a very important piece of information as it tells us that a successful disassembly of this binary will expose functions/variable that were used in its source, providing some pointers on how to solve this challenge. Before we move towards disassembly, let's run `strings` over this file as well:

Now this output is even more interesting since it exposes quite significant details about the challenge. First, it didn't show any commonly used buffer overflow prone libc functions like `gets` or `strcpy`, but just `puts`, `printf`, `read`, etc. There could be a [format-string](http://en.wikipedia.org/wiki/Uncontrolled_format_string) issue in the program (`printf`-family functions are likely [vulnerable](https://security.web.cern.ch/security/recommendations/en/codetools/c.shtml) if incorrectly used) but that can only be confirmed during static analysis of program disassembly or via dynamic analysis with multiple format-string prone inputs. But there's a bigger hint here: strings at the bottom following function names look interesting. Especially the `KFFSE_XHKYOKXOHOFEDM^E_Y` string since it looks like some kind of a key. May be the program mutates user-supplied input and performs a comparison with static flags like this string. If it does, we need to look at its disassembly and figure out the logic behind the mutation function and try to reverse it. Let's use `objdump` to disassemble this binary and dump its disassembly in [Intel syntax](http://en.wikipedia.org/wiki/X86_assembly_language#Syntax):

```c
$ objdump -d -M intel reverse-ex

reverse-ex:     file format elf32-i386

Disassembly of section .text:

080484c4 <checkkey>:
 80484c4: 55                    push   ebp
 80484c5: 89 e5                 mov    ebp,esp
 80484c7: 57                    push   edi
 80484c8: 56                    push   esi
 80484c9: 83 ec 10              sub    esp,0x10
 80484cc: 8b 45 08              mov    eax,DWORD PTR [ebp+0x8]
 80484cf: 89 45 f4              mov    DWORD PTR [ebp-0xc],eax
 80484d2: eb 14                 jmp    80484e8 <checkkey+0x24>
 80484d4: 8b 45 f4              mov    eax,DWORD PTR [ebp-0xc]
 80484d7: 0f b6 00              movzx  eax,BYTE PTR [eax]
 80484da: 89 c2                 mov    edx,eax
 80484dc: 83 f2 2a              xor    edx,0x2a
 80484df: 8b 45 f4              mov    eax,DWORD PTR [ebp-0xc]
 80484e2: 88 10                 mov    BYTE PTR [eax],dl
 80484e4: 83 45 f4 01           add    DWORD PTR [ebp-0xc],0x1
 80484e8: 8b 45 f4              mov    eax,DWORD PTR [ebp-0xc]
 80484eb: 0f b6 00              movzx  eax,BYTE PTR [eax]
 80484ee: 84 c0                 test   al,al
 80484f0: 75 e2                 jne    80484d4 <checkkey+0x10>
 80484f2: 8b 45 08              mov    eax,DWORD PTR [ebp+0x8]
 80484f5: 89 c2                 mov    edx,eax
 80484f7: b8 70 87 04 08        mov    eax,0x8048770
 80484fc: b9 19 00 00 00        mov    ecx,0x19
 8048501: 89 d6                 mov    esi,edx
 8048503: 89 c7                 mov    edi,eax
 8048505: f3 a6                 repz cmps BYTE PTR ds:[esi],BYTE PTR es:[edi]
 8048507: 0f 97 c2              seta   dl
 804850a: 0f 92 c0              setb   al
 804850d: 89 d1                 mov    ecx,edx
 804850f: 28 c1                 sub    cl,al
 8048511: 89 c8                 mov    eax,ecx
 8048513: 0f be c0              movsx  eax,al
 8048516: 85 c0                 test   eax,eax
 8048518: 75 07                 jne    8048521 <checkkey+0x5d>
 804851a: b8 01 00 00 00        mov    eax,0x1
 804851f: eb 05                 jmp    8048526 <checkkey+0x62>
 8048521: b8 00 00 00 00        mov    eax,0x0
 8048526: 83 c4 10              add    esp,0x10
 8048529: 5e                    pop    esi
 804852a: 5f                    pop    edi
 804852b: 5d                    pop    ebp
 804852c: c3                    ret

0804852d <foo>:
 804852d: 55                    push   ebp
 804852e: 89 e5                 mov    ebp,esp
 8048530: 83 ec 18              sub    esp,0x18
 8048533: c7 04 24 89 87 04 08  mov    DWORD PTR [esp],0x8048789
 804853a: e8 91 fe ff ff        call   80483d0 <puts@plt>
 804853f: b8 00 00 00 00        mov    eax,0x0
 8048544: c9                    leave
 8048545: c3                    ret

08048546 <bar>:
 8048546: 55                    push   ebp
 8048547: 89 e5                 mov    ebp,esp
 8048549: 83 ec 18              sub    esp,0x18
 804854c: c7 04 24 8d 87 04 08  mov    DWORD PTR [esp],0x804878d
 8048553: e8 78 fe ff ff        call   80483d0 <puts@plt>
 8048558: b8 00 00 00 00        mov    eax,0x0
 804855d: c9                    leave
 804855e: c3                    ret

0804855f <foobar>:
 804855f: 55                    push   ebp
 8048560: 89 e5                 mov    ebp,esp
 8048562: 83 ec 18              sub    esp,0x18
 8048565: 8b 45 08              mov    eax,DWORD PTR [ebp+0x8]
 8048568: 89 04 24              mov    DWORD PTR [esp],eax
 804856b: e8 bd ff ff ff        call   804852d <foo>
 8048570: b8 00 00 00 00        mov    eax,0x0
 8048575: c9                    leave
 8048576: c3                    ret

08048577 <main>:
 8048577: 55                    push   ebp
 8048578: 89 e5                 mov    ebp,esp
 804857a: 57                    push   edi
 804857b: 83 e4 f0              and    esp,0xfffffff0
 804857e: 81 ec 30 02 00 00     sub    esp,0x230
 8048584: b8 91 87 04 08        mov    eax,0x8048791
 8048589: 89 04 24              mov    DWORD PTR [esp],eax
 804858c: e8 1f fe ff ff        call   80483b0 <printf@plt>
 8048591: a1 40 a0 04 08        mov    eax,ds:0x804a040
 8048596: 89 04 24              mov    DWORD PTR [esp],eax
 8048599: e8 22 fe ff ff        call   80483c0 <fflush@plt>
 804859e: c7 44 24 08 ff 01 00  mov    DWORD PTR [esp+0x8],0x1ff
 80485a5: 00
 80485a6: 8d 44 24 24           lea    eax,[esp+0x24]
 80485aa: 89 44 24 04           mov    DWORD PTR [esp+0x4],eax
 80485ae: c7 04 24 00 00 00 00  mov    DWORD PTR [esp],0x0
 80485b5: e8 e6 fd ff ff        call   80483a0 <read@plt>
 80485ba: 8d 44 24 24           lea    eax,[esp+0x24]
 80485be: c7 44 24 1c ff ff ff  mov    DWORD PTR [esp+0x1c],0xffffffff
 80485c5: ff
 80485c6: 89 c2                 mov    edx,eax
 80485c8: b8 00 00 00 00        mov    eax,0x0
 80485cd: 8b 4c 24 1c           mov    ecx,DWORD PTR [esp+0x1c]
 80485d1: 89 d7                 mov    edi,edx
 80485d3: f2 ae                 repnz scas al,BYTE PTR es:[edi]
 80485d5: 89 c8                 mov    eax,ecx
 80485d7: f7 d0                 not    eax
 80485d9: 83 e8 01              sub    eax,0x1
 80485dc: 89 84 24 28 02 00 00  mov    DWORD PTR [esp+0x228],eax
 80485e3: 8b 84 24 28 02 00 00  mov    eax,DWORD PTR [esp+0x228]
 80485ea: 83 e8 01              sub    eax,0x1
 80485ed: 0f b6 44 04 24        movzx  eax,BYTE PTR [esp+eax*1+0x24]
 80485f2: 3c 0a                 cmp    al,0xa
 80485f4: 75 0f                 jne    8048605 <main+0x8e>
 80485f6: 8b 84 24 28 02 00 00  mov    eax,DWORD PTR [esp+0x228]
 80485fd: 83 e8 01              sub    eax,0x1
 8048600: c6 44 04 24 00        mov    BYTE PTR [esp+eax*1+0x24],0x0
 8048605: 0f b6 44 24 24        movzx  eax,BYTE PTR [esp+0x24]
 804860a: 0f be c0              movsx  eax,al
 804860d: 83 f8 42              cmp    eax,0x42
 8048610: 74 17                 je     8048629 <main+0xb2>
 8048612: 83 f8 43              cmp    eax,0x43
 8048615: 74 1f                 je     8048636 <main+0xbf>
 8048617: 83 f8 41              cmp    eax,0x41
 804861a: 75 27                 jne    8048643 <main+0xcc>
 804861c: c7 84 24 2c 02 00 00  mov    DWORD PTR [esp+0x22c],0x804852d
 8048623: 2d 85 04 08
 8048627: eb 1c                 jmp    8048645 <main+0xce>
 8048629: c7 84 24 2c 02 00 00  mov    DWORD PTR [esp+0x22c],0x80484c4
 8048630: c4 84 04 08
 8048634: eb 0f                 jmp    8048645 <main+0xce>
 8048636: c7 84 24 2c 02 00 00  mov    DWORD PTR [esp+0x22c],0x804855f
 804863d: 5f 85 04 08
 8048641: eb 02                 jmp    8048645 <main+0xce>
 8048643: eb fe                 jmp    8048643 <main+0xcc>
 8048645: 8d 44 24 24           lea    eax,[esp+0x24]
 8048649: 83 c0 01              add    eax,0x1
 804864c: 89 04 24              mov    DWORD PTR [esp],eax
 804864f: 8b 84 24 2c 02 00 00  mov    eax,DWORD PTR [esp+0x22c]
 8048656: ff d0                 call   eax
 8048658: 89 84 24 24 02 00 00  mov    DWORD PTR [esp+0x224],eax
 804865f: 83 bc 24 24 02 00 00  cmp    DWORD PTR [esp+0x224],0x0
 8048666: 00
 8048667: 74 1a                 je     8048683 <main+0x10c>
 8048669: b8 af 87 04 08        mov    eax,0x80487af
 804866e: 8d 54 24 24           lea    edx,[esp+0x24]
 8048672: 83 c2 01              add    edx,0x1
 8048675: 89 54 24 04           mov    DWORD PTR [esp+0x4],edx
 8048679: 89 04 24              mov    DWORD PTR [esp],eax
 804867c: e8 2f fd ff ff        call   80483b0 <printf@plt>
 8048681: eb 0c                 jmp    804868f <main+0x118>
 8048683: c7 04 24 be 87 04 08  mov    DWORD PTR [esp],0x80487be
 804868a: e8 41 fd ff ff        call   80483d0 <puts@plt>
 804868f: 8b 84 24 24 02 00 00  mov    eax,DWORD PTR [esp+0x224]
 8048696: 89 04 24              mov    DWORD PTR [esp],eax
 8048699: e8 52 fd ff ff        call   80483f0 <exit@plt>
 804869e: 90                    nop
 804869f: 90                    nop
```

I've removed certain non-important sections from the above output. Apart from `main`, there are 4 functions, namely `checkkey`, `foo`, `bar`, `foobar`. The `main` function includes certain anti-disassembly and obfuscation code and it's difficult to make proper sense of what's happening here. But let's focus on the important instructions. The `cmp` set of instructions starting at 0x804860d are interesting, especially the first `cmp` itself since it will cause a jump to 0x8048629 if the input buffer starts with 0x42 (B in ascii) and 0x8048629 is from where the `checkkey` function starts. Of all the available functions, `checkkey` is of obvious interest and this tells us that the program will only transfer control to `checkkey` function if the input starts with ascii `B` and not otherwise. Once the control reaches `checkkey` it will try to mutate input buffer and compare it against a static key. Let's conclude this analysis by having a closer look at `checkkey`'s disassembly:

```c
080484c4 <checkkey>:
 80484c4: 55                    push   ebp
 80484c5: 89 e5                 mov    ebp,esp
 80484c7: 57                    push   edi
 80484c8: 56                    push   esi
 80484c9: 83 ec 10              sub    esp,0x10
 80484cc: 8b 45 08              mov    eax,DWORD PTR [ebp+0x8]
 80484cf: 89 45 f4              mov    DWORD PTR [ebp-0xc],eax
 80484d2: eb 14                 jmp    80484e8 <checkkey+0x24>
 80484d4: 8b 45 f4              mov    eax,DWORD PTR [ebp-0xc]
 80484d7: 0f b6 00              movzx  eax,BYTE PTR [eax]
 80484da: 89 c2                 mov    edx,eax
 80484dc: 83 f2 2a              xor    edx,0x2a
 80484df: 8b 45 f4              mov    eax,DWORD PTR [ebp-0xc]
 80484e2: 88 10                 mov    BYTE PTR [eax],dl
 80484e4: 83 45 f4 01           add    DWORD PTR [ebp-0xc],0x1
 80484e8: 8b 45 f4              mov    eax,DWORD PTR [ebp-0xc]
 80484eb: 0f b6 00              movzx  eax,BYTE PTR [eax]
 80484ee: 84 c0                 test   al,al
 80484f0: 75 e2                 jne    80484d4 <checkkey+0x10>
 80484f2: 8b 45 08              mov    eax,DWORD PTR [ebp+0x8]
 80484f5: 89 c2                 mov    edx,eax
 80484f7: b8 70 87 04 08        mov    eax,0x8048770
 80484fc: b9 19 00 00 00        mov    ecx,0x19
 8048501: 89 d6                 mov    esi,edx
 8048503: 89 c7                 mov    edi,eax
 8048505: f3 a6                 repz cmps BYTE PTR ds:[esi],BYTE PTR es:[edi]
 8048507: 0f 97 c2              seta   dl
 804850a: 0f 92 c0              setb   al
 804850d: 89 d1                 mov    ecx,edx
 804850f: 28 c1                 sub    cl,al
 8048511: 89 c8                 mov    eax,ecx
 8048513: 0f be c0              movsx  eax,al
 8048516: 85 c0                 test   eax,eax
 8048518: 75 07                 jne    8048521 <checkkey+0x5d>
 804851a: b8 01 00 00 00        mov    eax,0x1
 804851f: eb 05                 jmp    8048526 <checkkey+0x62>
 8048521: b8 00 00 00 00        mov    eax,0x0
 8048526: 83 c4 10              add    esp,0x10
 8048529: 5e                    pop    esi
 804852a: 5f                    pop    edi
 804852b: 5d                    pop    ebp
 804852c: c3                    ret
```

After the [function prologue](http://en.wikipedia.org/wiki/Function_prologue), the `checkkey` function is reading the input buffer (starting address at `DWORD PTR [ebp+0x8]`) and performs a per-byte XOR using 0x2a as the key. Once the XOR operation completes, it is indeed comparing the resultant string with a pre-defined flag of size `0x19 - 1` bytes stored at 0x8048770. The `mov` instructions starting at address 0x80484f2 and the `repz cmps` instruction at address 0x8048505 confirm this analysis.

So we now know that the input will be XOR'ed with a static per-byte key of 0x2a and the result will be compared with a flag defined at 0x80484f2. To reverse this mutation logic the only remaining piece of information is the flag. If we obtain the flag and reverse the XOR operation, we'll have a string that will be accepted by the program for the challenge to complete. From the `strings` output earlier, we found a static key-like string, `KFFSE_XHKYOKXOHOFEDM^E_Y`, which looks like a very good candidate. Let's try to reverse the XOR operation using this string as the key and 0x2a as XOR key:

```python
#!/usr//bin/env python

import sys

if len(sys.argv) != 3:
    print "USAGE: %s <KFFSE_XHKYOKXOHOFEDM^E_Y> <0x2a>" % (sys.argv[0])
    sys.exit(1)

flag = sys.argv[1]
key = int(sys.argv[2], 16)
decoded = []

for c in flag:
    decoded.append(chr(ord(c) ^ key))

decoded = "".join(decoded)
print "%s ^ 0x%x => %s" % (flag, key, decoded)
```

```
$ ./xor.py KFFSE_XHKYOKXOHOFEDM^E_Y 0x2a
KFFSE_XHKYOKXOHOFEDM^E_Y ^ 0x2a => allyourbasearebelongtous
$
$ ./reverse-ex
Are you feeling lucky today? Ballyourbasearebelongtous
[+] WooT!: KFFSE_XHKYOKXOHOFEDM^E_Y
```

Awesome! First run of the program and we get a *WooT!* message confirming successful completion of this challenge. It can't get better than this.

Every assumption we made (`B` at the start of input, mutation logic based on a static key 0x2a, etc.) about the program was validated via static analysis except for the flag string used above. We assumed it to be the XOR result comparison flag stored at address 0x8048505 but didn't validate it in anyway except for trying it out with the binary itself. Authors of such challenges often add such strings to confuse the analyst and delay the process. However, validating this assumption is fairly trivial and let's see how to do it. Since, the value stored at this address could be static or dynamically-computed at runtime, let's use rely on the debugging process to provide us the correct result. We'll debug the program using GDB and check the contents of this address to validate our assumption:

```c
$ gdb ./reverse-ex -q
Reading symbols from /home/ankur/toolbox/challenges/misc/reverse-ex...(no debugging symbols found)...done.
(gdb)
(gdb) break checkkey
Breakpoint 1 at 0x80484c9
(gdb)
(gdb) r
Starting program: /home/ankur/toolbox/challenges/misc/reverse-ex
Are you feeling lucky today? BABCD

Breakpoint 1, 0x080484c9 in checkkey ()
(gdb)
(gdb) disas checkkey
Dump of assembler code for function checkkey:
   0x080484c4 <+0>: push   %ebp
   0x080484c5 <+1>: mov    %esp,%ebp
   0x080484c7 <+3>: push   %edi
   0x080484c8 <+4>: push   %esi
=> 0x080484c9 <+5>: sub    $0x10,%esp
   0x080484cc <+8>: mov    0x8(%ebp),%eax
   0x080484cf <+11>:  mov    %eax,-0xc(%ebp)
   0x080484d2 <+14>:  jmp    0x80484e8 <checkkey+36>
   0x080484d4 <+16>:  mov    -0xc(%ebp),%eax
   0x080484d7 <+19>:  movzbl (%eax),%eax
   0x080484da <+22>:  mov    %eax,%edx
   0x080484dc <+24>:  xor    $0x2a,%edx
   0x080484df <+27>:  mov    -0xc(%ebp),%eax
   0x080484e2 <+30>:  mov    %dl,(%eax)
   0x080484e4 <+32>:  addl   $0x1,-0xc(%ebp)
   0x080484e8 <+36>:  mov    -0xc(%ebp),%eax
   0x080484eb <+39>:  movzbl (%eax),%eax
   0x080484ee <+42>:  test   %al,%al
   0x080484f0 <+44>:  jne    0x80484d4 <checkkey+16>
   0x080484f2 <+46>:  mov    0x8(%ebp),%eax
   0x080484f5 <+49>:  mov    %eax,%edx
   0x080484f7 <+51>:  mov    $0x8048770,%eax
   0x080484fc <+56>:  mov    $0x19,%ecx
   0x08048501 <+61>:  mov    %edx,%esi
   0x08048503 <+63>:  mov    %eax,%edi
   0x08048505 <+65>:  repz cmpsb %es:(%edi),%ds:(%esi)
   0x08048507 <+67>:  seta   %dl
   0x0804850a <+70>:  setb   %al
   0x0804850d <+73>:  mov    %edx,%ecx
   0x0804850f <+75>:  sub    %al,%cl
   0x08048511 <+77>:  mov    %ecx,%eax
   0x08048513 <+79>:  movsbl %al,%eax
   0x08048516 <+82>:  test   %eax,%eax
   0x08048518 <+84>:  jne    0x8048521 <checkkey+93>
   0x0804851a <+86>:  mov    $0x1,%eax
   0x0804851f <+91>:  jmp    0x8048526 <checkkey+98>
   0x08048521 <+93>:  mov    $0x0,%eax
   0x08048526 <+98>:  add    $0x10,%esp
   0x08048529 <+101>: pop    %esi
   0x0804852a <+102>: pop    %edi
   0x0804852b <+103>: pop    %ebp
   0x0804852c <+104>: ret
End of assembler dump.
(gdb) x /s 0x8048770
0x8048770:   "KFFSE_XHKYOKXOHOFEDM^E_Y"
(gdb) q
A debugging session is active.

  Inferior 1 [process 13283] will be killed.

Quit anyway? (y or n) y
```

## Conclusion

We add a breakpoint at `checkkey` function and manually inspect the content of the 0x8048770 address (it might change on our system) and it indeed turns out to be `KFFSE_XHKYOKXOHOFEDM^E_Y`. This concludes this writeup and in an [upcoming post](https://7h3ram.github.io/posts/20130829_malsoftware-reverse-challenge.html) I'll write about the second challenge from this course.
