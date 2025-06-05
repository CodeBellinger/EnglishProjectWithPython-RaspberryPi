import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 256, auto_write=False)
width = 16
height = 16

def map_pixel(x: int, y: int) -> int:
	if(y < height/2):
		return(int(width*height-x*height/2+y-8))
	else:
		return(int(x*height/2+height-y-1))
      
def show():
    time.sleep(0.01)
    pixels.show()

def set_xy(pixel: tuple, color: tuple):
    pixels[map_pixel(pixel[0],pixel[1])] = color

def set_i(pixel: int, color: tuple):
    pixels[pixel] = color

def set_m(pixel_list: list):
    for pixel in pixel_list:
        pixels[map_pixel(pixel.x,pixel.y)] = pixel_list[pixel]
    show()

def fill(color: tuple):
    pixels.fill(color)
    show()

def fade(color: tuple):
    for i in range(len(pixels)):
        pixels[i] = (pixels[i][0]*color[0], pixels[i][1]*color[1], pixels[i][2]*color[2])
    show()

def max_value() -> int:
    max_p = max(range(len(pixels)), key=lambda i: sum(pixels[i]))
    return max_p, pixels[max_p]