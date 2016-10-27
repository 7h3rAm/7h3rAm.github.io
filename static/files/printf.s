# printf.s
# sample program to print "you win!\n" message to stdout

.section .text
.globl _start

_start:
  jmp cali

init:
  xorl %eax, %eax
  xorl %ebx, %ebx
  xorl %edx, %edx
  mov $4, %al
  mov $1, %bl
  popl %ecx
  mov $9, %dl
  int $0x80

  xorl %eax, %eax
  incl %eax
  xorl %ebx, %ebx
  int $0x80

cali:
  call init

msg:
  .ascii "you win!\n"
