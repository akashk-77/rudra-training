#include <stdio.h>
#include "maths_add.h"

int main() {
    int num1, num2, result;

    
    printf("Enter first number: ");
    scanf("%d", &num1);

    printf("Enter second number: ");
    scanf("%d", &num2);

    
    result = add(num1, num2);

    
    printf("Sum: %d\n", result);

    return 0;
}
