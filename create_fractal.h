typedef struct _Img{
    int width;
    int height;
    int * data;
} cImg;



int create_fractal(cImg img, int iters);
int mandel(float real, float imag, int max_iters, unsigned char * val);

