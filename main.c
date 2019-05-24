#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "create_fractal.h"

#ifdef CLOCK_PROCESS_CPUTIME_ID
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
#endif

int main(int argc, const char *argv[], const char * env[])
{
    int width = 1500;
    int height = 1000;
    int iters = 20;
    FILE * fid = NULL;
    cImg img;
#ifdef CLOCK_PROCESS_CPUTIME_ID
    struct timespec vartime;
#endif
    long time_elapsed_nanos;
    img.width = width;
    img.height = height;
    size_t written;
    img.data = (unsigned char*)malloc(width * height * sizeof(unsigned char));
    if (NULL == img.data)
        return -1;

#ifdef CLOCK_PROCESS_CPUTIME_ID
    vartime = timer_start();
#endif
    create_fractal(img, iters);
#ifdef CLOCK_PROCESS_CPUTIME_ID
    time_elapsed_nanos = timer_end(vartime);
    fprintf(stdout, "create_fractal required %ld millisecs\n", time_elapsed_nanos / 1000000);
#else
    fprintf(stdout, "create_fractal,  timing not available on this platform");
#endif

    fid = fopen("c.raw", "wb");
    if (NULL == fid)
        return -2;
    written = fwrite(img.data, sizeof(unsigned char), width * height, fid);
    fclose(fid);
    return 0;
}
