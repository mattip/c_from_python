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