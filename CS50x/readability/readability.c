#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{

    // ask user for text
string text = get_string("Text: ");


    //figure out the number of letters
float letter_count = 0.;
float word_count = 1.;
float sentence_count = 0.;

for( int i = 0; i < strlen(text); i++)
    {
        if(isalpha(text[i]))
        {
            letter_count++;
        }



        if(isspace(text[i]))
        {
            word_count++;
        }

        if(text[i] == 63 || text[i] == 46)
        {
            sentence_count++;
        }
    }

float L = (letter_count / word_count) * 100;
float S = (sentence_count / word_count) * 100;


    //coleman liau index - determine reading grade
    float index = roundf(0.0588 * L - 0.296 * S - 15.8);


    //print out grade
    if( index < 1 )
    {
    printf("Before Grade 1\n");
    }

    else if( index >= 16)
    {
    printf("Grade 16+\n");
    }

    else
    {
    printf("Grade %i\n", (int)index);
    }

}