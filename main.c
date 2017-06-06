#include <stdio.h>

int mandel(int x, int y, int max_iters, unsigned char * val);

void create_fractal(unsigned char * image, int width, int height, 
                    int iters);

int write_pbm(unsigned char * image, int width, int height, char * fname)
{
    int cnt;
    FILE * fid = fopen(fname, "wb");
    if (NULL == fid)
        return -1;
    cnt = f
}
int main(int argc, const char *argv[], const char * env[])
{
    return 0;
}
