#include <stdio.h>
#include "maths_add.h"

int add(int a, int b) {
    return a + b;
}

int main() {
    int flag;

    printf("Hello World\n");

    printf("Enter a number: ");
    scanf("%d", &flag);

    if (flag == 0) {
        int num1, num2;
        printf("Input is 0. Running add function...\n");

        printf("Enter first number: ");
        scanf("%d", &num1);

        printf("Enter second number: ");
        scanf("%d", &num2);

        int result = add(num1, num2);
        printf("Sum: %d\n", result);
    } else {
        printf("Input is not 0. Skipping add function.\n");
    }

    return 0;
}
