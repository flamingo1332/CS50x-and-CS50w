#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{

// error 1  no key
    if(argc != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }

// error 2  not 26
    if(strlen(argv[1]) != 26)
    {
        printf("Key must containt 26 characters\n");
        return 1;
    }

// error 3
// you can't use strings as argument of isalpha, you need a loop to check each character of the string.
    if(strlen(argv[1]) == 26)
    {
        for( int i = 0; i <= 25; i++) //loop
        {
            if (!isalpha(argv[1][i])) // if argv[1][i] is non-alphabet, print error
            {
            printf("Key must only contain alphabetic characters\n");
            return 1;
            }
        }
        for(int i = 0; i <= 24; i++) //loop
        {
            for(int h = i + 1; h <= 25; h++)
            {
                if (toupper(argv[1][i]) == toupper(argv[1][h])) //if ~
                {
                printf("Key must not contain repeated characters\n");
                return 1;
                }
            }
        }
    }

// KEY
    int key[25]; //key 0 ~ 25, A ~ Z 26 total  key[0] is A key

    for( int i = 0; i <= 25; i++) //loop 26
    {
        key[i] = toupper(argv[1][i]) - 65 - i;  // number between 0 ~ 25
    }

// input
    string plaintext = get_string("plaintext= ");

// output
    printf("ciphertext: ");

    for( int i = 0; i < strlen(plaintext); i++)
    {
        if(isupper(plaintext[i]))
        {
            for( int j = 0; j <= 25; j++)
            {
                if(plaintext[i] == 65 + j ) //만약 j가 2이면, 즉 plaintext가 c라면
                {
                    printf("%c", plaintext[i] + key[j]); //key 2를 부여 key 2 는 25, 즉 67더하기 25는 92
                }
            }
        }
        else if(islower(plaintext[i]))
        {
            for( int j = 0; j <= 25; j++)
            {
                if(plaintext[i] == 97 + j ) // 만약 텍스트가 c 라면 (j 2일때) 23
                {
                    printf("%c", plaintext[i] + key[j]);
                }
            }
        }
        else if(isdigit(plaintext[i]) || isspace(plaintext[i]) )
            {
                printf("%c", plaintext[i]);
            }
    }
    printf("\n");
    }






