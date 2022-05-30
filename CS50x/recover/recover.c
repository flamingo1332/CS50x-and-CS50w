#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

//buffer는 fread한 파일로부터 데이터를 저장해놓을 array다. array는 주소임
//fread를 하면 발생하는 일이 buffer(buffer는 array고 array는 주소임)의 주소에 fread된 데이터를 옮기고 fwrite하면 buffer에서 새로운 파일로 데이터를 옮기는것 pointer를 지정해주는 방식으로



int main(int argc, char *argv[])
{
//check usage
    if (argc != 2)
    {
        return 1;
    }

 //Open memory card,

    FILE* file = fopen(argv[1],"r");

    if (!file)
    {
        return 1;
    }



uint8_t buffer[512];
char* filename = malloc(8*sizeof(char)); //buffer 8 bytes allocated for filename
// char filename[8];                           //buffer 8 bytes allocated for filename
// start를 발견

FILE* img = NULL;  //NULL로 지정해줘야 한다고함 이유 찾아봐
int i = 0;

while(fread(buffer,sizeof(uint8_t), 512, file) == 512) //loop until end of memory card,  512bytes(per Block) per loop // 메모리 빈곳은 0으로 채워져있기때문에 512인곳까지가 메모리 끝
{

    if(buffer[0] == 0xff &&
       buffer[1] == 0xd8 &&
       buffer[2] == 0xff &&
      (buffer[3] & 0xf0) == 0xe0) //if start of a new jpeg..
    {

        if(i == 0)                                                          //if start of first jpeg...
        {
        sprintf(filename, "%03i.jpg", i);                                                       //create a new  img file

        img = fopen(filename, "w");
        fwrite(buffer,sizeof(uint8_t), 512, img);
        i = i + 1;
        }

        else                                                                                    //if start of jpeg(not first jpeg)...
        {
        fclose(img);     //close img file befor making new one

        sprintf(filename, "%03i.jpg", i);                                                       //create a new  img file
        img = fopen(filename, "w");
        fwrite(buffer,sizeof(uint8_t), 512, img);

        i = i + 1;
        }
    }

    else if(i != 0)                                                                        // if not start of jpeg... keep writing
    // 이게 segmentation fault나는 문제였음 instruction을 잘 봐야함 이게 필요한 이유는
    //card.raw 의 처음부터 바로 jpeg가 시작하지 않기 때문에 jpeg시작부분이 아니고 + 이어쓰기도 아닌데 fwrite해버리니 문제생기는 거였음
    // 처음부터 무조건 fwrite시작하면 안됌. syntax문제 아니라 논리구조 문제였음
    {
            fwrite(buffer,sizeof(uint8_t), 512, img);
    }

}

//close all files
free(filename);
fclose(img);
fclose(file);
return 0;
}



