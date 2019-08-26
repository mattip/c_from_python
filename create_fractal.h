#pragma once
typedef struct _Img{
    int width;
    int height;
    unsigned char * data;
} Img;


#ifdef _MSC_VER
#define EXPORT __declspec( dllexport )
#else
#define EXPORT
#endif
EXPORT
int create_fractal(Img img, int iters);
EXPORT
int mandel(float real, float imag, int max_iters, unsigned char * val);

