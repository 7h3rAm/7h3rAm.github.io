Eindbazen CTF Challenge: bin100
===============================
date: 27/May/2015
summary: This post is a writeup for the bin100 challenge (Dice Revenge) from Eindbazen CTF 2013.
tags: code, ctf, reversing

From the [challenges page](http://ebctf.nl/challenges/), download the [bin100](/static/files/bin100) binary and start following along. The challenge title is "Dice Revenge" and the description talks about Linux debugging skills. Let's see what `file` commands tells us about this file:

```bash
$ file bin100
bin100: ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.26, BuildID[sha1]=b07165d860e4c153770483d43e42a54f92f5ac93, not stripped
```

Alright, an ELF file. Let's issue a customary `strings` command on the challenge file:

```bash
$ strings bin100
/lib/ld-linux.so.2
CyIk
libstdc++.so.6
_ITM_deregisterTMCloneTable
__gmon_start__
_Jv_RegisterClasses
_ITM_registerTMCloneTable
pthread_cancel
_ZNKSs4sizeEv
_ZNKSs4findEPKcj
_ZNSsixEj
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_
_ZSt4cout
_ZNSaIcED1Ev
_ZNSsC1Ev
_ZNSolsEi
_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
_ZNSsC1EPKcRKSaIcE
_ZNSt8ios_base4InitC1Ev
_ZSt3cin
_ZNSsD1Ev
_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E
_ZNKSs6lengthEv
_ZNSt8ios_base4InitD1Ev
_ZNSsaSEPKc
_ZNSolsEPFRSoS_E
__gxx_personality_v0
_ZNSaIcEC1Ev
_ZSt7getlineIcSt11char_traitsIcESaIcEERSt13basic_istreamIT_T0_ES7_RSbIS4_S5_T1_E
libm.so.6
libgcc_s.so.1
_Unwind_Resume
libc.so.6
_IO_stdin_used
srand
time
__cxa_atexit
__libc_start_main
GCC_3.0
GLIBC_2.1.3
GLIBC_2.0
CXXABI_1.3
GLIBCXX_3.4
PTRh
QVhL
D$Xf
T$X1
D$lk
D$lA
l$lA
D$lk
T$l1
[^_]
 -------
|       |
|   O   |
|       |
 -------
 -------
|     O |
|       |
| O     |
 -------
 -------
|     O |
|   O   |
| O     |
 -------
 -------
| O   O |
|       |
| O   O |
 -------
 -------
| O   O |
|   O   |
| O   O |
 -------
 -------
| O   O |
| O   O |
| O   O |
 -------
 -------
| O   O |
| O O O |
| O   O |
 -------
[*] ebCTF 2013 - BIN100 - Dice Game
    To get the flag you will need to throw the correct numbers.
[*] You will first need to throw a three, press enter to throw a dice!
[*] You rolled a three! Good!
hZCnFH#i
\.&[?8i
fY0Q|9
?y^/%
[*] You rolled a
 That is not a three :/
[*] Game over!
[*] Next you will need to throw a one, press enter to throw a dice!
[*] You rolled a one! Very nice!
 That is not a one :/
[*] Next you will need to throw another three, press enter to throw a dice!
[*] You rolled a three! Awesome!
[*] Throw another three for me now, press enter to throw a dice!
[*] You rolled another three! Almost there now!
[*] The last character you need to roll is a seven....  (o_O)  Press enter to throw a dice!
[*] You rolled a seven, with a six sided dice! How awesome are you?!
 That is not a seven :/
ebCTF
[*] You rolled 3-1-3-3-7, what does that make you? ELEET! \o/
[*] Nice job, here is the flag:
[!] It seems you did something wrong :( No flag for you.
;*2$"
zPLR
GCC: (Debian 4.7.2-5) 4.7.2
GCC: (Debian 4.4.7-3) 4.4.7
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.gcc_except_table
.init_array
.fini_array
.jcr
.dynamic
.got
.got.plt
.data
.bss
.comment
crtstuff.c
__JCR_LIST__
deregister_tm_clones
register_tm_clones
__do_global_dtors_aux
completed.5730
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
bin100.c
_ZStL8__ioinit
_Z41__static_initialization_and_destruction_0ii
_GLOBAL__sub_I_main
_ZZL18__gthread_active_pvE20__gthread_active_ptr
__FRAME_END__
__JCR_END__
_GLOBAL_OFFSET_TABLE_
__init_array_end
__init_array_start
_DYNAMIC
data_start
_ZSt3cin@@GLIBCXX_3.4
_ZNSsaSEPKc@@GLIBCXX_3.4
_ZNSsC1Ev@@GLIBCXX_3.4
srand@@GLIBC_2.0
_ZNSolsEi@@GLIBCXX_3.4
__cxa_atexit@@GLIBC_2.1.3
__libc_csu_fini
_start
_ZSt7getlineIcSt11char_traitsIcESaIcEERSt13basic_istreamIT_T0_ES7_RSbIS4_S5_T1_E@@GLIBCXX_3.4
__gmon_start__
_Jv_RegisterClasses
_fp_hw
_ZNSsixEj@@GLIBCXX_3.4
_fini
_ZNKSs4sizeEv@@GLIBCXX_3.4
_ZNSt8ios_base4InitC1Ev@@GLIBCXX_3.4
__libc_start_main@@GLIBC_2.0
_ZNKSs6lengthEv@@GLIBCXX_3.4
_ZNSt8ios_base4InitD1Ev@@GLIBCXX_3.4
_ZNKSs4findEPKcj@@GLIBCXX_3.4
_ITM_deregisterTMCloneTable
_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@@GLIBCXX_3.4
_IO_stdin_used
_ZNSsD1Ev@@GLIBCXX_3.4
_ITM_registerTMCloneTable
__data_start
__TMC_END__
_ZNSsC1EPKcRKSaIcE@@GLIBCXX_3.4
_ZSt4cout@@GLIBCXX_3.4
__dso_handle
__libc_csu_init
time@@GLIBC_2.0
__bss_start
_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@@GLIBCXX_3.4
_ZNSaIcED1Ev@@GLIBCXX_3.4
pthread_cancel
_end
_ZNSolsEPFRSoS_E@@GLIBCXX_3.4
rand@@GLIBC_2.0
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_@@GLIBCXX_3.4
_edata
_ZNSaIcEC1Ev@@GLIBCXX_3.4
__gxx_personality_v0@@CXXABI_1.3
_Unwind_Resume@@GCC_3.0
__i686.get_pc_thunk.bx
main
_init
```

Quite a few interesting strings here. The title makes sense now. This looks like a dice game that requires us to throw certain number sequences to win. Let's give it a test run:

```bash
$ ./bin100

[*] ebCTF 2013 - BIN100 - Dice Game
    To get the flag you will need to throw the correct numbers.

[*] You will first need to throw a three, press enter to throw a dice!

 -------
|       |
|   O   |
|       |
 -------

[*] You rolled a 1 That is not a three :/
[*] Game over!
$
$ ./bin100

[*] ebCTF 2013 - BIN100 - Dice Game
    To get the flag you will need to throw the correct numbers.

[*] You will first need to throw a three, press enter to throw a dice!

 -------
|     O |
|   O   |
| O     |
 -------

[*] You rolled a three! Good!

[*] Next you will need to throw a one, press enter to throw a dice!

 -------
|     O |
|       |
| O     |
 -------

[*] You rolled a 2 That is not a one :/
[*] Game over!
$
$ ./bin100

[*] ebCTF 2013 - BIN100 - Dice Game
    To get the flag you will need to throw the correct numbers.

[*] You will first need to throw a three, press enter to throw a dice!

 -------
| O   O |
|   O   |
| O   O |
 -------

[*] You rolled a 5 That is not a three :/
[*] Game over!
```

Alright, looks like the first two numbers are `3` and `1` respectively. We might need multiple invocations to know further numbers in the expected sequence. Let's debug the file using GDB:

```bash
$ gdb -q ./bin100
Reading symbols from ./bin100...(no debugging symbols found)...done.
gdb-peda$ break *main
Breakpoint 1 at 0x8048c4c
gdb-peda$
```

Alright, now let's run the binary and when the breakpoint is hit, we can disassemble the `main` function:

```asm
gdb-peda$ r
Starting program: /media/shiv/red_third/stoolbox/challenges/ebctf/bin100/bin100
[----------------------------------registers-----------------------------------]
EAX: 0x1
EBX: 0xf7e5a000 --> 0x1a9da8
ECX: 0xa8769374
EDX: 0xffffb5b4 --> 0xf7e5a000 --> 0x1a9da8
ESI: 0x0
EDI: 0x0
EBP: 0x0
ESP: 0xffffb58c --> 0xf7cc9a83 (<__libc_start_main+243>:    mov    DWORD PTR [esp],eax)
EIP: 0x8048c4c (<main>: push   ebp)
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048c41 <frame_dummy+33>:  leave
   0x8048c42 <frame_dummy+34>:  jmp    0x8048bc0 <register_tm_clones>
   0x8048c47 <frame_dummy+39>:  jmp    0x8048bc0 <register_tm_clones>
=> 0x8048c4c <main>:    push   ebp
   0x8048c4d <main+1>:  mov    ebp,esp
   0x8048c4f <main+3>:  push   esi
   0x8048c50 <main+4>:  push   ebx
   0x8048c51 <main+5>:  and    esp,0xfffffff0
[------------------------------------stack-------------------------------------]
0000| 0xffffb58c --> 0xf7cc9a83 (<__libc_start_main+243>:   mov    DWORD PTR [esp],eax)
0004| 0xffffb590 --> 0x1
0008| 0xffffb594 --> 0xffffb624 --> 0xffffb82e ("/media/shiv/red_third/stoolbox/challenges/ebctf/bin100/bin100")
0012| 0xffffb598 --> 0xffffb62c --> 0xffffb86c ("GREP_COLOR=1;33")
0016| 0xffffb59c --> 0xf7feacea (add    ebx,0x12316)
0020| 0xffffb5a0 --> 0x1
0024| 0xffffb5a4 --> 0xffffb624 --> 0xffffb82e ("/media/shiv/red_third/stoolbox/challenges/ebctf/bin100/bin100")
0028| 0xffffb5a8 --> 0xffffb5c4 --> 0xce293764
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x08048c4c in main ()
gdb-peda$  pdisas main
Dump of assembler code for function main:
=> 0x08048c4c <+0>: push   ebp
   0x08048c4d <+1>: mov    ebp,esp
   0x08048c4f <+3>: push   esi
   0x08048c50 <+4>: push   ebx
   0x08048c51 <+5>: and    esp,0xfffffff0
   0x08048c54 <+8>: sub    esp,0x70
   0x08048c57 <+11>:    lea    eax,[esp+0x3c]
   0x08048c5b <+15>:    mov    DWORD PTR [esp],eax
   0x08048c5e <+18>:    call   0x80489d0 <_ZNSsC1Ev@plt>
   0x08048c63 <+23>:    mov    DWORD PTR [esp+0x6c],0x5
   0x08048c6b <+31>:    lea    eax,[esp+0x38]
   0x08048c6f <+35>:    mov    DWORD PTR [esp],eax
   0x08048c72 <+38>:    call   0x80489d0 <_ZNSsC1Ev@plt>
   0x08048c77 <+43>:    lea    eax,[esp+0x34]
   0x08048c7b <+47>:    mov    DWORD PTR [esp],eax
   0x08048c7e <+50>:    call   0x80489d0 <_ZNSsC1Ev@plt>
   0x08048c83 <+55>:    mov    DWORD PTR [esp],0x0
   0x08048c8a <+62>:    call   0x8048ad0 <time@plt>
   0x08048c8f <+67>:    mov    DWORD PTR [esp],eax
   0x08048c92 <+70>:    call   0x80489e0 <srand@plt>
   0x08048c97 <+75>:    lea    eax,[esp+0x41]
   0x08048c9b <+79>:    mov    DWORD PTR [esp],eax
   0x08048c9e <+82>:    call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048ca3 <+87>:    lea    eax,[esp+0x41]
   0x08048ca7 <+91>:    mov    DWORD PTR [esp+0x8],eax
   0x08048cab <+95>:    mov    DWORD PTR [esp+0x4],0x8049e40
   0x08048cb3 <+103>:   lea    eax,[esp+0x30]
   0x08048cb7 <+107>:   mov    DWORD PTR [esp],eax
   0x08048cba <+110>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048cbf <+115>:   lea    eax,[esp+0x41]
   0x08048cc3 <+119>:   mov    DWORD PTR [esp],eax
   0x08048cc6 <+122>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048ccb <+127>:   lea    eax,[esp+0x42]
   0x08048ccf <+131>:   mov    DWORD PTR [esp],eax
   0x08048cd2 <+134>:   call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048cd7 <+139>:   lea    eax,[esp+0x42]
   0x08048cdb <+143>:   mov    DWORD PTR [esp+0x8],eax
   0x08048cdf <+147>:   mov    DWORD PTR [esp+0x4],0x8049e74
   0x08048ce7 <+155>:   lea    eax,[esp+0x2c]
   0x08048ceb <+159>:   mov    DWORD PTR [esp],eax
   0x08048cee <+162>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048cf3 <+167>:   lea    eax,[esp+0x42]
   0x08048cf7 <+171>:   mov    DWORD PTR [esp],eax
   0x08048cfa <+174>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048cff <+179>:   lea    eax,[esp+0x43]
   0x08048d03 <+183>:   mov    DWORD PTR [esp],eax
   0x08048d06 <+186>:   call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048d0b <+191>:   lea    eax,[esp+0x43]
   0x08048d0f <+195>:   mov    DWORD PTR [esp+0x8],eax
   0x08048d13 <+199>:   mov    DWORD PTR [esp+0x4],0x8049ea8
   0x08048d1b <+207>:   lea    eax,[esp+0x28]
   0x08048d1f <+211>:   mov    DWORD PTR [esp],eax
   0x08048d22 <+214>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048d27 <+219>:   lea    eax,[esp+0x43]
   0x08048d2b <+223>:   mov    DWORD PTR [esp],eax
   0x08048d2e <+226>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048d33 <+231>:   lea    eax,[esp+0x44]
   0x08048d37 <+235>:   mov    DWORD PTR [esp],eax
   0x08048d3a <+238>:   call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048d3f <+243>:   lea    eax,[esp+0x44]
   0x08048d43 <+247>:   mov    DWORD PTR [esp+0x8],eax
   0x08048d47 <+251>:   mov    DWORD PTR [esp+0x4],0x8049edc
   0x08048d4f <+259>:   lea    eax,[esp+0x24]
   0x08048d53 <+263>:   mov    DWORD PTR [esp],eax
   0x08048d56 <+266>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048d5b <+271>:   lea    eax,[esp+0x44]
   0x08048d5f <+275>:   mov    DWORD PTR [esp],eax
   0x08048d62 <+278>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048d67 <+283>:   lea    eax,[esp+0x45]
   0x08048d6b <+287>:   mov    DWORD PTR [esp],eax
   0x08048d6e <+290>:   call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048d73 <+295>:   lea    eax,[esp+0x45]
   0x08048d77 <+299>:   mov    DWORD PTR [esp+0x8],eax
   0x08048d7b <+303>:   mov    DWORD PTR [esp+0x4],0x8049f10
   0x08048d83 <+311>:   lea    eax,[esp+0x20]
   0x08048d87 <+315>:   mov    DWORD PTR [esp],eax
   0x08048d8a <+318>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048d8f <+323>:   lea    eax,[esp+0x45]
   0x08048d93 <+327>:   mov    DWORD PTR [esp],eax
   0x08048d96 <+330>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048d9b <+335>:   lea    eax,[esp+0x46]
   0x08048d9f <+339>:   mov    DWORD PTR [esp],eax
   0x08048da2 <+342>:   call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048da7 <+347>:   lea    eax,[esp+0x46]
   0x08048dab <+351>:   mov    DWORD PTR [esp+0x8],eax
   0x08048daf <+355>:   mov    DWORD PTR [esp+0x4],0x8049f44
   0x08048db7 <+363>:   lea    eax,[esp+0x1c]
   0x08048dbb <+367>:   mov    DWORD PTR [esp],eax
   0x08048dbe <+370>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048dc3 <+375>:   lea    eax,[esp+0x46]
   0x08048dc7 <+379>:   mov    DWORD PTR [esp],eax
   0x08048dca <+382>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048dcf <+387>:   lea    eax,[esp+0x47]
   0x08048dd3 <+391>:   mov    DWORD PTR [esp],eax
   0x08048dd6 <+394>:   call   0x8048b30 <_ZNSaIcEC1Ev@plt>
   0x08048ddb <+399>:   lea    eax,[esp+0x47]
   0x08048ddf <+403>:   mov    DWORD PTR [esp+0x8],eax
   0x08048de3 <+407>:   mov    DWORD PTR [esp+0x4],0x8049f78
   0x08048deb <+415>:   lea    eax,[esp+0x18]
   0x08048def <+419>:   mov    DWORD PTR [esp],eax
   0x08048df2 <+422>:   call   0x8048ac0 <_ZNSsC1EPKcRKSaIcE@plt>
   0x08048df7 <+427>:   lea    eax,[esp+0x47]
   0x08048dfb <+431>:   mov    DWORD PTR [esp],eax
   0x08048dfe <+434>:   call   0x8048af0 <_ZNSaIcED1Ev@plt>
   0x08048e03 <+439>:   mov    DWORD PTR [esp+0x58],0x66
   0x08048e0b <+447>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048e13 <+455>:   mov    DWORD PTR [esp],0x804b780
   0x08048e1a <+462>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048e1f <+467>:   mov    DWORD PTR [esp+0x4],0x8049fac
   0x08048e27 <+475>:   mov    DWORD PTR [esp],eax
   0x08048e2a <+478>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08048e2f <+483>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048e37 <+491>:   mov    DWORD PTR [esp],0x804b780
   0x08048e3e <+498>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048e43 <+503>:   mov    DWORD PTR [esp+0x4],0x8049fd0
   0x08048e4b <+511>:   mov    DWORD PTR [esp],eax
   0x08048e4e <+514>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08048e53 <+519>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048e5b <+527>:   mov    DWORD PTR [esp],eax
   0x08048e5e <+530>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048e63 <+535>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048e6b <+543>:   mov    DWORD PTR [esp],eax
   0x08048e6e <+546>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048e73 <+551>:   mov    DWORD PTR [esp+0x4],0x804a010
   0x08048e7b <+559>:   mov    DWORD PTR [esp],0x804b780
   0x08048e82 <+566>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08048e87 <+571>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048e8f <+579>:   mov    DWORD PTR [esp],eax
   0x08048e92 <+582>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048e97 <+587>:   lea    eax,[esp+0x34]
   0x08048e9b <+591>:   mov    DWORD PTR [esp+0x4],eax
   0x08048e9f <+595>:   mov    DWORD PTR [esp],0x804b6e0
   0x08048ea6 <+602>:   call   0x8048a10 <_ZSt7getlineIcSt11char_traitsIcESaIcEERSt13basic_istreamIT_T0_ES7_RSbIS4_S5_T1_E@plt>
   0x08048eab <+607>:   mov    DWORD PTR [esp],0x0
   0x08048eb2 <+614>:   call   0x8048ad0 <time@plt>
   0x08048eb7 <+619>:   mov    DWORD PTR [esp+0x54],eax
   0x08048ebb <+623>:   call   0x8048b10 <rand@plt>
   0x08048ec0 <+628>:   mov    ecx,eax
   0x08048ec2 <+630>:   mov    edx,0x2aaaaaab
   0x08048ec7 <+635>:   mov    eax,ecx
   0x08048ec9 <+637>:   imul   edx
   0x08048ecb <+639>:   mov    eax,ecx
   0x08048ecd <+641>:   sar    eax,0x1f
   0x08048ed0 <+644>:   sub    edx,eax
   0x08048ed2 <+646>:   mov    eax,edx
   0x08048ed4 <+648>:   add    eax,eax
   0x08048ed6 <+650>:   add    eax,edx
   0x08048ed8 <+652>:   add    eax,eax
   0x08048eda <+654>:   mov    edx,ecx
   0x08048edc <+656>:   sub    edx,eax
   0x08048ede <+658>:   lea    eax,[edx+0x1]
<snip>
   0x08049d39 <+4333>:  mov    eax,ebx
   0x08049d3b <+4335>:  jmp    0x8049d3d <main+4337>
   0x08049d3d <+4337>:  mov    DWORD PTR [esp],eax
   0x08049d40 <+4340>:  call   0x8048b50 <_Unwind_Resume@plt>
   0x08049d45 <+4345>:  lea    esp,[ebp-0x8]
   0x08049d48 <+4348>:  pop    ebx
   0x08049d49 <+4349>:  pop    esi
   0x08049d4a <+4350>:  pop    ebp
   0x08049d4b <+4351>:  ret
End of assembler dump.
```

Analyzing this function is quite easy if you note the following block being repeated five times:

```asm
   0x08048ee1 <+661>:   mov    DWORD PTR [esp+0x50],eax
   0x08048ee5 <+665>:   cmp    DWORD PTR [esp+0x50],0x1
   0x08048eea <+670>:   jne    0x8048f00 <main+692>
   0x08048eec <+672>:   lea    eax,[esp+0x30]
   0x08048ef0 <+676>:   mov    DWORD PTR [esp+0x4],eax
   0x08048ef4 <+680>:   mov    DWORD PTR [esp],0x804b780
   0x08048efb <+687>:   call   0x8048ae0 <_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@plt>
   0x08048f00 <+692>:   cmp    DWORD PTR [esp+0x50],0x2
   0x08048f05 <+697>:   jne    0x8048f1b <main+719>
   0x08048f07 <+699>:   lea    eax,[esp+0x2c]
   0x08048f0b <+703>:   mov    DWORD PTR [esp+0x4],eax
   0x08048f0f <+707>:   mov    DWORD PTR [esp],0x804b780
   0x08048f16 <+714>:   call   0x8048ae0 <_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@plt>
   0x08048f1b <+719>:   cmp    DWORD PTR [esp+0x50],0x3
   0x08048f20 <+724>:   jne    0x8048f36 <main+746>
   0x08048f22 <+726>:   lea    eax,[esp+0x28]
   0x08048f26 <+730>:   mov    DWORD PTR [esp+0x4],eax
   0x08048f2a <+734>:   mov    DWORD PTR [esp],0x804b780
   0x08048f31 <+741>:   call   0x8048ae0 <_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@plt>
   0x08048f36 <+746>:   cmp    DWORD PTR [esp+0x50],0x4
   0x08048f3b <+751>:   jne    0x8048f51 <main+773>
   0x08048f3d <+753>:   lea    eax,[esp+0x24]
   0x08048f41 <+757>:   mov    DWORD PTR [esp+0x4],eax
   0x08048f45 <+761>:   mov    DWORD PTR [esp],0x804b780
   0x08048f4c <+768>:   call   0x8048ae0 <_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@plt>
   0x08048f51 <+773>:   cmp    DWORD PTR [esp+0x50],0x5
   0x08048f56 <+778>:   jne    0x8048f6c <main+800>
   0x08048f58 <+780>:   lea    eax,[esp+0x20]
   0x08048f5c <+784>:   mov    DWORD PTR [esp+0x4],eax
   0x08048f60 <+788>:   mov    DWORD PTR [esp],0x804b780
   0x08048f67 <+795>:   call   0x8048ae0 <_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@plt>
   0x08048f6c <+800>:   cmp    DWORD PTR [esp+0x50],0x6
   0x08048f71 <+805>:   jne    0x8048f87 <main+827>
   0x08048f73 <+807>:   lea    eax,[esp+0x1c]
   0x08048f77 <+811>:   mov    DWORD PTR [esp+0x4],eax
   0x08048f7b <+815>:   mov    DWORD PTR [esp],0x804b780
   0x08048f82 <+822>:   call   0x8048ae0 <_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E@plt>
   0x08048f87 <+827>:   cmp    DWORD PTR [esp+0x50],0x3
   0x08048f8c <+832>:   jne    0x8048fdc <main+912>
   0x08048f8e <+834>:   mov    DWORD PTR [esp+0x4],0x804a057
   0x08048f96 <+842>:   mov    DWORD PTR [esp],0x804b780
   0x08048f9d <+849>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08048fa2 <+854>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048faa <+862>:   mov    DWORD PTR [esp],eax
   0x08048fad <+865>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048fb2 <+870>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08048fba <+878>:   mov    DWORD PTR [esp],eax
   0x08048fbd <+881>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08048fc2 <+886>:   shl    DWORD PTR [esp+0x6c],1
   0x08048fc6 <+890>:   mov    DWORD PTR [esp+0x4],0x804a078
   0x08048fce <+898>:   lea    eax,[esp+0x38]
   0x08048fd2 <+902>:   mov    DWORD PTR [esp],eax
   0x08048fd5 <+905>:   call   0x80489c0 <_ZNSsaSEPKc@plt>
   0x08048fda <+910>:   jmp    0x8049053 <main+1031>
   0x08048fdc <+912>:   mov    DWORD PTR [esp+0x4],0x804a0a0
   0x08048fe4 <+920>:   mov    DWORD PTR [esp],0x804b780
   0x08048feb <+927>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08048ff0 <+932>:   mov    edx,DWORD PTR [esp+0x50]
   0x08048ff4 <+936>:   mov    DWORD PTR [esp+0x4],edx
   0x08048ff8 <+940>:   mov    DWORD PTR [esp],eax
   0x08048ffb <+943>:   call   0x80489f0 <_ZNSolsEi@plt>
   0x08049000 <+948>:   mov    DWORD PTR [esp+0x4],0x804a0b2
   0x08049008 <+956>:   mov    DWORD PTR [esp],eax
   0x0804900b <+959>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08049010 <+964>:   mov    DWORD PTR [esp+0x4],0x8048b20
   0x08049018 <+972>:   mov    DWORD PTR [esp],eax
   0x0804901b <+975>:   call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08049020 <+980>:   mov    DWORD PTR [esp+0x4],0x804a0ca
   0x08049028 <+988>:   mov    DWORD PTR [esp],0x804b780
   0x0804902f <+995>:   call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08049034 <+1000>:  mov    DWORD PTR [esp+0x4],0x8048b20
   0x0804903c <+1008>:  mov    DWORD PTR [esp],eax
   0x0804903f <+1011>:  call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x08049044 <+1016>:  mov    ebx,0x0
   0x08049049 <+1021>:  mov    esi,0x0
   0x0804904e <+1026>:  jmp    0x8049b00 <main+3764>
   0x08049053 <+1031>:  mov    DWORD PTR [esp],0x0
   0x0804905a <+1038>:  call   0x8048ad0 <time@plt>
   0x0804905f <+1043>:  mov    DWORD PTR [esp+0x4c],eax
   0x08049063 <+1047>:  mov    eax,DWORD PTR [esp+0x54]
   0x08049067 <+1051>:  mov    edx,DWORD PTR [esp+0x4c]
   0x0804906b <+1055>:  mov    ecx,edx
   0x0804906d <+1057>:  sub    ecx,eax
   0x0804906f <+1059>:  mov    eax,ecx
   0x08049071 <+1061>:  mov    DWORD PTR [esp+0x48],eax
   0x08049075 <+1065>:  cmp    DWORD PTR [esp+0x48],0x2
   0x0804907a <+1070>:  jle    0x8049080 <main+1076>
   0x0804907c <+1072>:  shl    DWORD PTR [esp+0x6c],1
   0x08049080 <+1076>:  mov    DWORD PTR [esp+0x4],0x804a0dc
   0x08049088 <+1084>:  mov    DWORD PTR [esp],0x804b780
   0x0804908f <+1091>:  call   0x8048aa0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08049094 <+1096>:  mov    DWORD PTR [esp+0x4],0x8048b20
   0x0804909c <+1104>:  mov    DWORD PTR [esp],eax
   0x0804909f <+1107>:  call   0x8048b00 <_ZNSolsEPFRSoS_E@plt>
   0x080490a4 <+1112>:  lea    eax,[esp+0x34]
   0x080490a8 <+1116>:  mov    DWORD PTR [esp+0x4],eax
   0x080490ac <+1120>:  mov    DWORD PTR [esp],0x804b6e0
   0x080490b3 <+1127>:  call   0x8048a10 <_ZSt7getlineIcSt11char_traitsIcESaIcEERSt13basic_istreamIT_T0_ES7_RSbIS4_S5_T1_E@plt>
   0x080490b8 <+1132>:  mov    DWORD PTR [esp],0x0
   0x080490bf <+1139>:  call   0x8048ad0 <time@plt>
   0x080490c4 <+1144>:  mov    DWORD PTR [esp+0x54],eax
   0x080490c8 <+1148>:  call   0x8048b10 <rand@plt>
   0x080490cd <+1153>:  mov    ecx,eax
   0x080490cf <+1155>:  mov    edx,0x2aaaaaab
   0x080490d4 <+1160>:  mov    eax,ecx
   0x080490d6 <+1162>:  imul   edx
   0x080490d8 <+1164>:  mov    eax,ecx
   0x080490da <+1166>:  sar    eax,0x1f
   0x080490dd <+1169>:  sub    edx,eax
   0x080490df <+1171>:  mov    eax,edx
   0x080490e1 <+1173>:  add    eax,eax
   0x080490e3 <+1175>:  add    eax,edx
   0x080490e5 <+1177>:  add    eax,eax
   0x080490e7 <+1179>:  mov    edx,ecx
   0x080490e9 <+1181>:  sub    edx,eax
   0x080490eb <+1183>:  lea    eax,[edx+0x1]
```

Interestingly, these five blocks compare `EAX` (contains random value for the dice face) with expected value at each instance. If the dice (or the random number generator) has `3-1-3-3-7` values in sequence, we will get the flag.

We can solve this by patching the first instruction of each block (`0x08048ee1` in the above block) to load expected values into `EAX` rather than random values. This can be done in Python using the awesome [pwntools](https://github.com/Gallopsled/pwntools) library as follows:

```python
#!/usr/bin/env python2

import sys
from pwn import *

e = ELF('bin100')

addrvals = {
  0x08048ee1: 0x03,
  0x080490ee: 0x01,
  0x080492fc: 0x03,
  0x080494ff: 0x03,
  0x08049744: 0x07
}
for addr, value in addrvals.iteritems():
  print "0x%08x" % (addr)
  e.write(addr, asm("mov DWORD PTR [esp+0x50], %s" % (value), arch="i386"))
  print disasm(e.read(addr-0xf, 32))
  print

e.save('bin100.patched')
```

We create a mapping of expected values and addresses where these need to be written. Executing this script will create a new patched file that should then give us the flag:

```bash
$ ./bin100.patched

[*] ebCTF 2013 - BIN100 - Dice Game
    To get the flag you will need to throw the correct numbers.

[*] You will first need to throw a three, press enter to throw a dice!

 -------
|       |
|   O   |
|       |
 -------

 -------
|     O |
|   O   |
| O     |
 -------

[*] You rolled a three! Good!

[*] Next you will need to throw a one, press enter to throw a dice!

 -------
|       |
|   O   |
|       |
 -------

[*] You rolled a one! Very nice!

[*] Next you will need to throw another three, press enter to throw a dice!

 -------
|       |
|   O   |
|       |
 -------

 -------
|     O |
|   O   |
| O     |
 -------

[*] You rolled a three! Awesome!

[*] Throw another three for me now, press enter to throw a dice!

 -------
|       |
|   O   |
|       |
 -------

 -------
|     O |
|   O   |
| O     |
 -------

[*] You rolled another three! Almost there now!

[*] The last character you need to roll is a seven....  (o_O)  Press enter to throw a dice!

 -------
|       |
|   O   |
|       |
 -------

 -------
| O   O |
| O O O |
| O   O |
 -------

[*] You rolled a seven, with a six sided dice! How awesome are you?!

[*] You rolled 3-1-3-3-7, what does that make you? ELEET! \o/
[*] Nice job, here is the flag: ebCTF{9a9689dbd47a1fd3fc0bf17d60edf545}
```

Awesome! We sucessfully solve this challenge and are presented with the flag. You can download the patched file [here](/static/files/bin100.patched).
