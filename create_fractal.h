typedef struct _Img{
    int width;
    int height;
    unsigned char * data;
} cImg;



int create_fractal(cImg img, int iters);
int mandel(float real, float imag, int max_iters, unsigned char * val);

