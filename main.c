#include <stdio.h>
#include <pgm.h>
#include <time.h>

// call this function to start a nanosecond-resolution timer
struct timespec timer_start(){
    struct timespec start_time;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_time);
    return start_time;
}

// call this function to end a timer, returning nanoseconds elapsed as a long
long timer_end(struct timespec start_time){
    struct timespec end_time;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_time);
    long diffInNanos = end_time.tv_nsec - start_time.tv_nsec;
    return diffInNanos;
}

int mandel(int x, int y, int max_iters, unsigned int * val);

void create_fractal(unsigned int * image, int width, int height, 
                    int iters);

int main(int argc, const char *argv[], const char * env[])
{
    int width = 1500;
    int height = 1000;
    int iters = 20;
    FILE * fid = NULL;
    struct timespec vartime;
    long time_elapsed_nanos;
    unsigned int * image = (unsigned int*)malloc(width * height * sizeof(unsigned int));
    if (NULL == image)
        return -1;
    fid = fopen("c.pgm", "wb");
    if (NULL == fid)
        return -2;
    vartime = timer_start();
    create_fractal(image, width, height, iters);
    time_elapsed_nanos = timer_end(vartime);
    fprintf(stdout, "create_fractal required %ld millisecs\n", time_elapsed_nanos / 1000000);
    pgm_writepgminit(fid, width, height, 255, 0);
    for (int i=0; i<height; i++)
        pgm_writepgmrow(fid, image + width*i, width, 255, 0);
    fclose(fid);
    return 0;
}
