/* stack2.c                                     *
 * specially crafted to feed your brain by gera */

int main() {
    int cookie;
    char buf[80];

    printf("buf: %08x cookie: %08x\n", &buf, &cookie);
    gets(buf);

    if (cookie == 0x01020305)
        printf("you win!\n");
}