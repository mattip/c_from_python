from __future__ import print_function, division
import subprocess
import os

width = 1500
height = 1000
#ctypes
# First all the declarations. Each function and struct must be redefined ...
import ctypes

class CtypesImg(ctypes.Structure):
    _fields_ = [('width', ctypes.c_int),
                ('height', ctypes.c_int),
                ('data', ctypes.POINTER(ctypes.c_uint8)), # HUH?
               ]
    array_cache = {}
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Create a class type to hold the data.
        # Since this creates a type, cache it for reuse rather
        # than create a new one each time
        if width*height not in self.array_cache:
            self.array_cache[width*height] = ctypes.c_uint8 * (width * height)
        # Note this keeps the img.data alive in the interpreter
        self.data = self.array_cache[width*height]() # !!!!!!

    def asmemoryview(self):
        # There must be a better way, but this code will not
        # be timed, so explicit trumps implicit
        ret = self.array_cache[width*height]()
        for i in range(width*height):
            ret[i] = self.data[i]
        return ret

ctypesimg = CtypesImg(width, height)

    
# Load the DLL
cdll = ctypes.cdll.LoadLibrary('./libcreate_fractal.so')

#Fish the function pointers from the DLL and define the interfaces
create_fractal_ctypes = cdll.create_fractal
create_fractal_ctypes.argtypes = [CtypesImg, ctypes.c_int]

mandel_ctypes = cdll.mandel
mandel_ctypes.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_int, 
                          ctypes.POINTER(ctypes.c_uint8)]


if __name__ == "__main__":
    from timeit import default_timer as timer
    from PIL import Image
    from create_fractal import create_fractal
    s = timer()
    create_fractal_ctypes(ctypesimg, 20)
    e = timer()
    ctypes_onecall = e - s
    print('ctypes calling create_fractal required {:.2f} millisecs'.format(1000*ctypes_onecall))
    data = ctypesimg.asmemoryview()
    print(max(data))
    im = Image.frombuffer("L", (width, height), data, 'raw', 'L', 0, 1)
    im.save('ctypes_fractal.png')

    value = (ctypes.c_uint8*1)()
    s = timer()
    create_fractal(ctypesimg, 20, mandel_ctypes, value)
    e = timer()
    ctypes_createfractal = e - s
    data = ctypesimg.asmemoryview()
    print(max(data))
    print('ctypes calling mandel required {:.2f} millisecs'.format(1000*ctypes_createfractal))
    im = Image.frombuffer("L", (width, height), data, 'raw', 'L', 0, 1)
    im.save('ctypes_mandel.png')
