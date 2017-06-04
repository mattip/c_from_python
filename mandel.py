#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

'''
Taken from https://github.com/numba/numba/blob/master/examples/mandel/mandel_jit.py
On June 3, 2017, then modified by mattip
Original copyright:

Copyright (c) 2012, Continuum Analytics, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Contact GitHub API Training Shop Blog About 

'''

from timeit import default_timer as timer

import sys
fname = 'test'
if len(sys.argv) > 1 and 'nojit' in sys.argv[1]:
   def jit(f):
        print('pure python')
        return f
   fname = 'test_nojit'
else:
   from numba import jit
   fname = 'test_numba'


@jit
def mandel(x, y, max_iters):
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
            return i

    return 255

@jit
def create_fractal(min_x, max_x, min_y, max_y, image, width, height, iters):
    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for y in range(height):
        imag = min_y + y * pixel_size_y
        yy = y*width
        for x in range(width):
            real = min_x + x * pixel_size_x
            color = mandel(real, imag, iters)
            image[yy+x] = color

    return image

width = 1500
height = 1000
if 'cffi' in sys.argv:
    import cffi
    ffi = cffi.FFI()
    image = ffi.new('unsigned char[{}]'.format(width*height))
    img_as_bytes = bytes(ffi.buffer(image, width*height))
    fname += '_cffi'
else:
    import numpy as np
    image = np.empty(width*height, dtype=np.uint8)
    fname += '_numpy'
    img_as_bytes = image
s = timer()
create_fractal(-2.0, 1.0, -1.0, 1.0, image, width, height, 20)
e = timer()
print(e - s)
if 0:
    from matplotlib.pylab import imshow, jet, show, ion
    imshow(image)
    show()
else:
    from PIL import Image
    try:
        im = Image.frombuffer('L', (width, height), img_as_bytes, 'raw', 'L', 0, 1)
        im.save(fname + '.png')
    except:
        import traceback;traceback.print_exc()
        import pdb;pdb.set_trace()
