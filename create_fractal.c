int mandel(float x, float y, int max_iters, unsigned char * val);

typedef struct _Img{
    int width;
    int height;
    unsigned char * data;
} Img;


void create_fractal(Img img,  int iters) {
    float pixel_size_x = 3.0 / img.width;
    float pixel_size_y = 2.0 / img.height;
    for (int y=0; y < img.height; y++) {
        float imag = y * pixel_size_y - 1;
        int yy = y * img.width;
        for (int x=0; x < img.width; x++) {
            float real = x * pixel_size_x - 2;
            unsigned char color;
            int ret = mandel(real, imag, iters, &color);
            img.data[yy + x] = color;
        }
    }
}
