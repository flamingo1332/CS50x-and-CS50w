#include <math.h>
#include <stdio.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height ; i ++)
        {
            for(int j = 0; j < width; j++)
        {
            float c_average = roundf(((image[i][j].rgbtRed+image[i][j].rgbtGreen+image[i][j].rgbtBlue)/3.0));
            // 나눌 때 3쓰면 integer로 나누는거라 결과도 int로 나옴. 그래서 부정확함. int아닌 결과 원하면 나누는 수도 3.0이렇게 표현해야함
            image[i][j].rgbtRed = c_average;
            image[i][j].rgbtGreen = c_average;
            image[i][j].rgbtBlue = c_average;
        }
        }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for( int i = 0; i < height ; i++)
    {
        for( int j = 0; j < (width/2) ; j++)
        {
            RGBTRIPLE temp;
            temp = image[i][j];
            image[i][j] = image[i][width-j-1];
            image[i][width-j-1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

// blur순차적으로 처리하면 나머지 영향받으므로 array 에 별도로 저장
int RED[height][width];
int BLUE[height][width];
int GREEN[height][width];
// 계속 안되던 이유 = int RGB [][]가 height-1 와 width-1 로 설정되어 있었는데 height와 width로 바꿔주니까 제대로 됌 이걸로 2시간날림 이유 정확히 뭔지 모르겠음

float c_average_RED;
float c_average_Green;
float c_average_Blue;

    for( int i = 0; i < height ; i++)
    {
        for( int j = 0; j < width; j++)
        {
            c_average_RED = 0.0;
            c_average_Green = 0.0;
            c_average_Blue = 0.0;

            // 4.0으로 나눔 모서리에 있다면
            if((i == 0 && j == 0)||(i == height-1 && j == width-1)||(i == 0 && j == width-1)||(i == height-1 && j == 0))
            {
                for( int h = i-1; h < i+2; h++)
                {
                    for( int w = j-1; w < j +2; w++)
                    {
                        if(0 <= h && h < height && 0 <= w && w < width )
                        {
                        c_average_RED = c_average_RED + image[h][w].rgbtRed;
                        c_average_Green = c_average_Green + image[h][w].rgbtGreen;
                        c_average_Blue = c_average_Blue + image[h][w].rgbtBlue;
                        }

                    }
                }
                c_average_RED = ((float)c_average_RED+2)/(float)4.0;
               c_average_Green = ((float)c_average_Green+2)/(float)4.0;
                c_average_Blue = ((float)c_average_Blue+2)/(float)4.0;
                float roundf(float c_average_RED);
                float roundf(float c_average_Green);
                float roundf(float c_average_Blue);

                RED[i][j] = c_average_RED;
                GREEN[i][j] = c_average_Green;
                BLUE[i][j] = c_average_Blue;
            }

            //6.0으로 나눔 모서리 아닌 사이드
            else if((i == 0 && j != 0 && j != width-1 )||(i == height-1 && j != 0 && j != width-1 )||(j == 0 && i != 0 && i != height-1 )||(j == width-1 && i != 0 && i != height-1 ))
            {
                for( int h = i-1; h < i+2; h++)
                {
                    for( int w = j-1; w < j +2; w++)
                    {
                        if(  0 <= h && h < height &&  0 <= w && w < width )
                        {
                        c_average_RED = c_average_RED + image[h][w].rgbtRed;
                        c_average_Green = c_average_Green + image[h][w].rgbtGreen;
                        c_average_Blue = c_average_Blue + image[h][w].rgbtBlue;
                        }

                    }
                }

                //Just as an alternative to his suggestion, you could avoid the conversions to and from floating point by adding half the divisor before the integer division, e. g.
                //나중에 다시 볼 것
               c_average_RED = ((float)c_average_RED+3)/(float)6.0;
               c_average_Green = ((float)c_average_Green+3)/(float)6.0;
                c_average_Blue = ((float)c_average_Blue+3)/(float)6.0;
                float roundf(float c_average_RED);
                float roundf(float c_average_Green);
                float roundf(float c_average_Blue);


                RED[i][j] = c_average_RED;
                GREEN[i][j] = c_average_Green;
                BLUE[i][j] = c_average_Blue;
            }

            //9.0으로 나눔 일반
            else if(i != 0 && i != height-1 && j != 0 && j != width-1)
            {
                for( int h = i-1; h < i+2; h++)
                {
                    for( int w = j-1; w < j +2; w++)
                    {
                        c_average_RED = c_average_RED + image[h][w].rgbtRed;
                        c_average_Green = c_average_Green + image[h][w].rgbtGreen;
                        c_average_Blue = c_average_Blue + image[h][w].rgbtBlue;
                    }
                }
                c_average_RED = ((float)c_average_RED+4)/(float)9.0;
               c_average_Green = ((float)c_average_Green+4)/(float)9.0;
                c_average_Blue = ((float)c_average_Blue+4)/(float)9.0;
                float roundf(float c_average_RED);
                float roundf(float c_average_Green);
                float roundf(float c_average_Blue);


                RED[i][j] = c_average_RED;
                GREEN[i][j] = c_average_Green;
                BLUE[i][j] = c_average_Blue;
            }
        }
    }

   for( int i = 0; i < height ; i++)
    {
        for( int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = RED[i][j];
            image[i][j].rgbtGreen = GREEN[i][j];
            image[i][j].rgbtBlue = BLUE[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
int RED[height][width];
int GREEN[height][width];
int BLUE[height][width];

float GxR[height][width];
float GxG[height][width];
float GxB[height][width];
float GyR[height][width];
float GyG[height][width];
float GyB[height][width];

RGBTRIPLE temp[height+2][width+2]; //declare 할때 숫자는 numbering과 관련없다. 즉 n개 declare 하면 0 부터 n-1까지 numbering 됨
//array가 0에서 height까진데 array[-1],[height+1] 등을 사용하면 이상해짐 직접 사용해서 해결하는 방법은 못찾겠어서 별도의 2d array를 만들어서 그 안에 image[][]를 배치함.

        for( int i = 0; i < height; i++)
        {
            for( int j = 0 ; j < width; j++)
            {
            temp[i+1][j+1].rgbtRed = image[i][j].rgbtRed;
            temp[i+1][j+1].rgbtGreen = image[i][j].rgbtGreen;
            temp[i+1][j+1].rgbtBlue = image[i][j].rgbtBlue;
            }
        }

            for( int i = 0; i < height + 2 ; i++)
        {
            temp[i][0].rgbtRed = 0;
            temp[i][0].rgbtGreen = 0;
            temp[i][0].rgbtBlue = 0;
            temp[i][width+1].rgbtRed = 0;
            temp[i][width+1].rgbtGreen = 0;
            temp[i][width+1].rgbtBlue = 0;
        }
            for( int i = 0; i < width + 2 ; i++)
        {
            temp[0][i].rgbtRed = 0;
            temp[0][i].rgbtGreen = 0;
            temp[0][i].rgbtBlue = 0;
            temp[height+1][i].rgbtRed = 0;
            temp[height+1][i].rgbtGreen = 0;
            temp[height+1][i].rgbtBlue = 0;
        }



    for( int i = 0; i < height ; i++)
    {
        for( int j = 0; j < width; j++)
        {
            GxR[i][j] = 0.0;
            GxG[i][j] = 0.0;
            GxB[i][j] = 0.0;
            GyR[i][j] = 0.0;
            GyG[i][j] = 0.0;
            GyB[i][j] = 0.0;



            GxR[i][j] = GxR[i][j] - temp[i][j].rgbtRed - (2 * temp[i+1][j].rgbtRed) - temp[i+2][j].rgbtRed + temp[i][j+2].rgbtRed + (2 * temp[i+1][j+2].rgbtRed) + temp[i+2][j+2].rgbtRed;
            GxG[i][j] = GxG[i][j] - temp[i][j].rgbtGreen - (2 * temp[i+1][j].rgbtGreen) - temp[i+2][j].rgbtGreen + temp[i][j+2].rgbtGreen + (2 * temp[i+1][j+2].rgbtGreen) + temp[i+2][j+2].rgbtGreen;
            GxB[i][j] = GxB[i][j] - temp[i][j].rgbtBlue - (2 * temp[i+1][j].rgbtBlue) - temp[i+2][j].rgbtBlue + temp[i][j+2].rgbtBlue + (2 * temp[i+1][j+2].rgbtBlue) + temp[i+2][j+2].rgbtBlue;

            GyR[i][j] = GyR[i][j] - temp[i][j].rgbtRed - (2 * temp[i][j+1].rgbtRed) - temp[i][j+2].rgbtRed + temp[i+2][j].rgbtRed + (2 * temp[i+2][j+1].rgbtRed) + temp[i+2][j+2].rgbtRed;
            GyG[i][j] = GyG[i][j] - temp[i][j].rgbtGreen - (2 * temp[i][j+1].rgbtGreen) - temp[i][j+2].rgbtGreen + temp[i+2][j].rgbtGreen + (2 * temp[i+2][j+1].rgbtGreen) + temp[i+2][j+2].rgbtGreen;
            GyB[i][j] = GyB[i][j] - temp[i][j].rgbtBlue - (2 * temp[i][j+1].rgbtBlue) - temp[i][j+2].rgbtBlue + temp[i+2][j].rgbtBlue + (2 * temp[i+2][j+1].rgbtBlue) + temp[i+2][j+2].rgbtBlue;


            // GxR[i][j] = GxR[i][j] - temp[i-1][j-1].rgbtRed - 2 * temp[i][j-1].rgbtRed - temp[i+1][j-1].rgbtRed + temp[i-1][j+1].rgbtRed + 2 * temp[i][j+1].rgbtRed + temp[i+1][j+1].rgbtRed;
            // GxG[i][j] = GxG[i][j] - temp[i-1][j-1].rgbtGreen - 2 * temp[i][j-1].rgbtGreen - temp[i+1][j-1].rgbtGreen + temp[i-1][j+1].rgbtGreen + 2 * temp[i][j+1].rgbtGreen + temp[i+1][j+1].rgbtGreen;
            // GxB[i][j] = GxB[i][j] - temp[i-1][j-1].rgbtBlue - 2 * temp[i][j-1].rgbtBlue - temp[i+1][j-1].rgbtBlue + temp[i-1][j+1].rgbtBlue + 2 * temp[i][j+1].rgbtBlue + temp[i+1][j+1].rgbtBlue;

            // GyR[i][j] = GyR[i][j] - temp[i-1][j-1].rgbtRed - 2 * temp[i-1][j].rgbtRed - temp[i-1][j+1].rgbtRed + temp[i+1][j-1].rgbtRed + 2 * temp[i+1][j].rgbtRed + temp[i+1][j+1].rgbtRed;
            // GyG[i][j] = GyG[i][j] - temp[i-1][j-1].rgbtGreen - 2 * temp[i-1][j].rgbtGreen - temp[i-1][j+1].rgbtGreen + temp[i+1][j-1].rgbtGreen + 2 * temp[i+1][j].rgbtGreen + temp[i+1][j+1].rgbtGreen;
            // GyB[i][j] = GyB[i][j] - temp[i-1][j-1].rgbtBlue - 2 * temp[i-1][j].rgbtBlue - temp[i-1][j+1].rgbtBlue + temp[i+1][j-1].rgbtBlue + 2 * temp[i+1][j].rgbtBlue + temp[i+1][j+1].rgbtBlue;






                RED[i][j] = roundf(sqrtf((GxR[i][j] * GxR[i][j]) + (GyR[i][j] * GyR[i][j])));
                GREEN[i][j] = roundf(sqrtf((GxG[i][j] * GxG[i][j]) + (GyG[i][j] * GyG[i][j])));
                BLUE[i][j] = roundf(sqrtf((GxB[i][j] * GxB[i][j]) + (GyB[i][j] * GyB[i][j])));

                if (RED[i][j] > 255)
                {
                    RED[i][j] = 255;
                }
                if (GREEN[i][j] > 255)
                {
                    GREEN[i][j] = 255;
                }
                if (BLUE[i][j] > 255)
                {
                    BLUE[i][j] = 255;
                }
            }
    }


   for( int i = 0; i < height ; i++)
    {
        for( int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = RED[i][j];
            image[i][j].rgbtGreen = GREEN[i][j];
            image[i][j].rgbtBlue = BLUE[i][j];
        }
    }
    return;
}

