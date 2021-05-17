reverse Challenge from Coursera's Malicious Software Course
===========================================================
date: 29/Aug/2013
summary: This is a writeup on the reverse-challenge from recently concluded Malicious Software course on Coursera.
tags: ctf, reversing

## Introduction

This post follows an earlier one: [reverse-ex Challenge from Coursera's Malicious Software Course](https://7h3ram.github.io/posts/20130824_malsoftware-reverse-ex.html). If you've not already read it, I would suggest you do so since both these challenges share a few common concepts and I'll be skipping detail if it has been mentioned before.

## Program Analysis and Testing

The challenge file is hosted here: [reverse-challenge](/static/files/posts_malsoftware_reverse_challenge/reverse-challenge). The first thing to do is to test it with `file` command:

```
$ file reverse-challenge
reverse-challenge: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[  sha1]=0x2fe5f1647532449ffeef36a7fa31ae8319c8818d, stripped
$
$ file -i reverse-challenge
reverse-challenge: application/x-executable; charset=binary
```

Like the previous challenge this is also a 32bit [ELF](http://en.wikipedia.org/wiki/Executable_and_Linkable_Format) binary, [dynamically linked](http://stackoverflow.com/questions/1993390/static-linking-vs-dynamic-linking), but a significant difference is that it has [symbols stripped](http://unix.stackexchange.com/questions/2969/what-are-stripped-and-not-stripped-executables-in-unix). This means that debugging and symbol resolution information has *NOT* been preserved within the binary. This loss of debugging information would be evident when we move on to static analysis part later but first let's see what `strings` has to tell us about this file:

If you've read the previous post this output would certainly delight you due to the discernible similarity between the two challenge files. Similar looking status strings and a static flag indicate that this program, like its predecessor, also uses some mutation mechanism (mostly XOR, but we will validate it soon) and a static key which we can use to reverse the algorithm. This time, let's use IDA to disassemble and analyze this program:

![image](/static/files/posts_malsoftware_reverse_challenge/ida-start.png.webp)

Since the program includes anti-reversing techniques, I tried to avoid traversing the code manually and quickly searched for the section referencing the flag we found in `strings` output: `xKZl_^_XCY^CIE`. It was found that this flag was being referenced at location 0x08048694. Before that, there was the code responsible for performing the mutation, which in this case was also XOR. However, instead of using a static value as a key, it was being computed at runtime. The `mov dword ptr [ebp-10h], 0FAh` and `and edx, 2Bh` instructions at locations 0x08048664 and 0x08048677 respectively initialized `edx` with a value of 0x2a which is then used in a XOR operation at location 0x0804867A.

![image](/static/files/posts_malsoftware_reverse_challenge/ida-checkkey.png.webp)

Thus the per-byte XOR key for this program turns out to be 0x2a. Let's invoke the python script we used in previous post with `xKZl_^_XCY^CIE` as the flag and 0x2a as the key and reverse the simple XOR mutation logic:

```
$ ./xor.py xKZl_^_XCY^CIE 0x2a
xKZl_^_XCY^CIE ^ 0x2a => RapFuturistico
$
$ ./reverse-challenge
Are you feeling lucky today? BRapFuturistico
[+] WooT!: xKZl_^_XCY^CIE
```

As expected, `RapFuturistico` indeed is the right input string derived from reversing the XOR-based mutation logic used in the program. Like earlier, we could have also tried debugging this program but the `Dude, no debugging ;-)` string from the `strings` output indicates presence of anti-debugging measures and I refrained using it in this challenge. It can be confirmed with a simple `strace` of the program:

```c
$ strace ./reverse-challenge
execve("./reverse-challenge", ["./reverse-challenge"], [/* 63 vars */]) = 0
[ Process PID=22998 runs in 32 bit mode. ]
brk(0)                                  = 0x9882000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
mmap2(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff76f5000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat64(3, {st_mode=S_IFREG|0644, st_size=156058, ...}) = 0
mmap2(NULL, 156058, PROT_READ, MAP_PRIVATE, 3, 0) = 0xfffffffff76ce000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/i386-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0000\226\1\0004\0\0\0"..., 512) = 512
fstat64(3, {st_mode=S_IFREG|0755, st_size=1734120, ...}) = 0
mmap2(NULL, 1743580, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0xfffffffff7524000
mmap2(0xf76c8000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1a4) = 0xfffffffff76c8000
mmap2(0xf76cb000, 10972, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xfffffffff76cb000
close(3)                                = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff7523000
set_thread_area(0xffbd0af0)             = 0
mprotect(0xf76c8000, 8192, PROT_READ)   = 0
mprotect(0x8049000, 4096, PROT_READ)    = 0
mprotect(0xf7718000, 4096, PROT_READ)   = 0
munmap(0xf76ce000, 156058)              = 0
ptrace(PTRACE_TRACEME, 4290579748, 0xffbd0cb4, 0) = -1 EPERM (Operation not permitted)
fstat64(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 5), ...}) = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff76f4000
write(1, "Dude, no debugging ;-)\n", 23Dude, no debugging ;-)
) = 23
exit_group(1)                           = ?
```

The program stopped since the `ptrace` system call returned `EPERM` error code which indicates that the `PTRACE_TRACEME` operation is not permitted. This is a very commonly used anti-debugging method and it works since such program already invoke `ptrace` over them before executing any other functions and as such when a user manually tries to debug it (via `ptrace` calls), it fails since a trace session is already active on the program and another cannot be initialized.

## Conclusion

Anyways, like the previous challenge, this was also completed without actually debugging the program. However, there are still ways in which we can bypass the anti-debugging mechanisms and analyze the program via dynamic analysis only. Rest on this in a future post. Stay tuned.
