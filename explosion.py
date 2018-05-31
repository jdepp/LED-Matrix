import sys
import time
import random
from threading import Thread, Lock

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 2
#options.brightness = 50
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Setting up colors
redColor = graphics.Color(255, 0, 0)
yellowColor = graphics.Color(255, 140, 0)
orangeColor = graphics.Color(255, 70, 0)
blueColor = graphics.Color(0, 0, 255)
greenColor = graphics.Color(0, 255, 0)
purpleColor = graphics.Color(128, 0, 128)
whiteColor = graphics.Color(255, 255, 255)
colors = [redColor, yellowColor, orangeColor, blueColor, greenColor, purpleColor, whiteColor]

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont('./fonts/4x6.bdf')

list_circles = []


class Circle:
    def __init__(self, x_val, y_val, r, c):
        self.x = x_val
        self.y = y_val
        self.radius = r
        self.color = c


def add_circle():
    while True:
        x = random.randint(2, 61)
        y = random.randint(2, 13)
        radius = 0
        idx = random.randint(0, len(colors)-1)
        color = colors[idx]
        list_circles.append(Circle(x, y, radius, color))
        time.sleep(0.25)


def check_radius():
    while True:
        for circle in list_circles:
            if(circle.radius == 9):
                list_circles.remove(circle)


try:
    print('Press CTRL-C to stop.')
    canvas = matrix.CreateFrameCanvas()
    thread1 = Thread(target=add_circle)
    thread2 = Thread(target=check_radius)
    thread1.daemon = True
    thread2.daemon = True
    thread1.start()
    thread2.start()
    while True:
        canvas.Clear()
        for circle in list_circles:
            index = random.randint(0, 6)
            current_color = circle.color
            graphics.DrawCircle(canvas, circle.x, circle.y, circle.radius, current_color)
            circle.radius = circle.radius + 1
        canvas = matrix.SwapOnVSync(canvas)
        time.sleep(0.125)


except KeyboardInterrupt:
    sys.exit(0)

