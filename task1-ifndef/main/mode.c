#include <stdio.h>

#ifndef MODE
#define MODE 0
#endif

#if MODE == 1
    #include "maths_add.h"

    int add(int a, int b) {
        return a + b;
    }
#endif

int main() {
    printf("Hello World\n");

#if MODE == 1
    int num1, num2;
    printf("\n--- Mode 1: Addition ---\n");

    printf("Enter first number: ");
    scanf("%d", &num1);

    printf("Enter second number: ");
    scanf("%d", &num2);

    printf("Sum: %d\n", add(num1, num2));

#elif MODE == 2
    printf("\n--- Mode 2: Exiting Program ---\n");
    return 0;

#else
    printf("\nNo valid mode selected at compile time (Use -DMODE=1 or -DMODE=2).\n");
#endif

    return 0;
}
