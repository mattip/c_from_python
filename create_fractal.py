from __future__ import print_function, division

from mandel import mandel

def create_fractal(image, width, height, iters):
    pixel_size_x = 3.0 / width
    pixel_size_y = 2.0 / height
    for y in range(height):
        imag = y * pixel_size_y - 1
        yy = y*width
        for x in range(width):
            real = x * pixel_size_x - 2
            color = mandel(real, imag, iters)
            image[yy+x] = color

if __name__ == '__main__':
    from timeit import default_timer as timer
    import numpy as np
    from PIL import Image
    width = 1500
    height = 1000
    image = np.empty(width*height, dtype=np.uint8)
    s = timer()
    create_fractal(image, width, height, 20)
    e = timer()
    print('pure python required {}f.2 secs'.format(e - s))
    im = Image.frombuffer('L', (width, height), image, 'raw', 'L', 0, 1)
    im.save('python_numpy.png') 
