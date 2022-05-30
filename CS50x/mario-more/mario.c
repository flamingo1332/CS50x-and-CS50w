#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;

    do
    {
    n = get_int("height(1~8): ");
    }

    while(n>8 || n<1);

    for(int i = 0, a=1; i < n; i++)
    {
        for(int h = 0; h < n-a; h++)
        {
        printf(" ");
        }

        for(int j = 0; j < a; j++)
        {
        printf("#");
        }

        printf("  ");

        for(int j = 0; j < a; j++)
        {
        printf("#");
        }

    printf("\n");

    a++;
    }
}