#And for desert:
import sys
print(sys.executable)
from timeit import default_timer as timer
import cffi
from PIL import Image

ffi = cffi.FFI()

class Img(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = ffi.new('uint8_t[%d]' % (width*height,))

def create_fractal(image, iters, func, oneval):
    ''' Call a function for each pixel in the image, where
        -2 < real < 1 over the columns and
        -1 < imag < 1 over the rows
    '''
    pixel_size_x = 3.0 / image.width
    pixel_size_y = 2.0 / image.height
    for y in range(image.height):
        imag = y * pixel_size_y - 1
        yy = y * image.width
        for x in range(image.width):
            real = x * pixel_size_x - 2
            func(real, imag, iters, oneval)
            image.data[yy + x] = oneval[0]

def mandel(x, y, max_iters, value):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    i = 0
    c = complex(x,y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            value[0] = i
            return 0
    value[0] = max_iters
    return max_iters

# Pure python
width = 1500
height = 1000
image = Img(width, height)
s = timer()
oneval = ffi.new('uint8_t[1]')
create_fractal(image, 20, mandel, oneval)
e = timer()
pure_pypy = e - s
print('pure pypy required {:.2f} millisecs'.format(pure_pypy))
im = Image.fromarray(image.data.reshape(height, width))
im.save('pypyy.png')