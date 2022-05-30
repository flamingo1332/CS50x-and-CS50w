#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long n = get_long("Number= ");

    int digit1 = n / 1000000000000000 % 10;
    int digit2 = n / 100000000000000 % 10;
    int digit3 = n / 10000000000000 % 10;
    int digit4 = n / 1000000000000 % 10;
    int digit5 = n / 100000000000 % 10;
    int digit6 = n / 10000000000 % 10;
    int digit7 = n / 1000000000 % 10;
    int digit8 = n / 100000000 % 10;
    int digit9 = n / 10000000 % 10;
    int digit10 = n / 1000000 % 10;
    int digit11 = n / 100000 % 10;
    int digit12 = n / 10000 % 10;
    int digit13 = n / 1000 % 10;
    int digit14 = n / 100 % 10;
    int digit15 = n / 10 % 10;
    int digit16 = n % 10;
    int count = 0;

    if(digit1 > 4)
    {
        count = count + 1;
    }

        if(digit3 > 4)
    {
        count = count + 1;
    }

        if(digit5 > 4)
    {
        count = count + 1;
    }

        if(digit7 > 4)
    {
        count = count + 1;
    }

        if(digit9 > 4)
    {
        count = count + 1;
    }

        if(digit11 > 4)
    {
        count = count + 1;
    }

        if(digit13 > 4)
    {
        count = count + 1;
    }

        if(digit15 > 4)
    {
        count = count + 1;
    }



    int a = digit15*2 + digit13*2 + digit11*2 + digit9*2 + digit7*2 + digit5*2 + digit3*2 + digit1*2 - count*9;
    int b = digit16 + digit14 + digit12 + digit10 + digit8 + digit6 + digit4 + digit2 + a;


// 16digit
    if(999999999999999<n && n<10000000000000000)
    {
        if(b % 10 == 0)
        {
        if(digit1*10 + digit2 == 51 ||digit1*10 + digit2 == 52 ||digit1*10 + digit2 == 53 ||digit1*10 + digit2 == 54 ||digit1*10 + digit2 == 55 )
        {
        printf("MASTERCARD\n");
        }
        else if(digit1 == 4)
        {
        printf("VISA\n");
        }
        else
        {
        printf("INVALID\n");
        }
    }
    else
    {
    printf("INVALID\n");
    }
    }

// 15digit
    if(99999999999999<n && n<1000000000000000)
    {
        if(b % 10 == 0)
        {

        if(digit2*10 + digit3 == 34 || digit2*10 + digit3 == 37 )
        {
        printf("AMEX\n");
        }
        else
        {
        printf("INVALID\n");
        }
        }

        else
        {
        printf("INVALID\n");
        }
    }

// 13digit
    if(999999999999<n && n<10000000000000)
    {
        if(b % 10 == 0 && digit4 == 4)
        {
        printf("VISA\n");
        }

        else
        {
        printf("INVALID\n");
        }
    }

    // under 12digit
    if(n<1000000000000)
    {
    printf("INVALID\n");
    }
    // over 16digit
    if(n>9999999999999999)
    {
    printf("INVALID\n");
    }
    // 14digit
    if(9999999999999<n && n<100000000000000)
    {
    printf("INVALID\n");
    }
}