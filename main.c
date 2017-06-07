#include <stdio.h>
#include <pbm.h>

int mandel(int x, int y, int max_iters, unsigned char * val);

void create_fractal(unsigned char * image, int width, int height, 
                    int iters);

int main(int argc, const char *argv[], const char * env[])
{
    int width = 1500;
    int height = 1000;
    int iters = 20;
    FILE * fid = NULL;
    unsigned char * image = (unsigned char*)malloc(width*height);
    if (NULL == image)
        return -1;
    fid = fopen("c.pbm", "wb");
    if (NULL == fid)
        return -2;
    create_fractal(image, width, height, iters);
    pbm_writepbminit(fid, width, height, 0);
    for (int i=0; i<height; i++)
        pbm_writepbmrow(fid, image + width*i, width, 0);
    fclose(fid);
    return 0;
}
