#include <stdio.h>;
#include <string.h>;

int main () {
    char array[80];

    printf ("&array: %p\n", &array);
    gets (array);
    printf ("*array: {\"%s\"}\n", array);

    return 0;
}
