#include <stdio.h>
#include "maths_add.h"

int add(int a, int b) {
    return a + b;
}


void run_addition_task(void) {
    int num1, num2;
    printf("Input is 0. Running addition task...\n");

    printf("Enter first number: ");
    scanf("%d", &num1);

    printf("Enter second number: ");
    scanf("%d", &num2);

    printf("Sum: %d\n", add(num1, num2));
}

int main() {
    int input;

    printf("Enter a number: ");
    scanf("%d", &input);

   
    if (input == 0) {
        run_addition_task();
    } else {
        printf("Input is not 0. Skipping addition task.\n");
    }

    return 0;
}
