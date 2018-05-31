import time
import sys
import os.path
from os import path

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

if(len(sys.argv) != 2):
    print("Need 1 arg: name of the file to be read")
    sys.exit(0)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

blueColor = graphics.Color(0, 0, 255)
redColor = graphics.Color(255, 0, 0)
yellowColor = graphics.Color(255, 204, 0)
greenColor = graphics.Color(0, 255, 0)
purpleColor = graphics.Color(127, 0, 255)
whiteColor = graphics.Color(255, 255, 255)

colors = [blueColor, redColor, yellowColor, greenColor, purpleColor, whiteColor]

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont('./fonts/6x13.bdf')
pos = offscreen_canvas.width
current_text = ""

try:
    i = 0
    current_color = blueColor
    print('Press CTRL-C to stop.')
    while True:
        if(path.isfile(sys.argv[1])):
            file_to_be_read = open(sys.argv[1], 'r')
            items_array = [line.strip() for line in file_to_be_read.readlines()]
            for item in items_array:
                current_color = colors[i % 6]
                while True:
                    offscreen_canvas.Clear()
                    len = graphics.DrawText(offscreen_canvas, font, pos, 12, current_color, item)
                    pos -= 1
                    if(pos + len < 0):
                        pos = offscreen_canvas.width
                        i += 1
                        if(i == 6):
                            i = 0
                        break
                    time.sleep(0.02)
                    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
except KeyboardInterrupt:
    sys.exit(0)
