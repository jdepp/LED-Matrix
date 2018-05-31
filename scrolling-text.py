##################################################################################################################
# THIS PROGRAM DISPLAYS TEXT THAT SCROLLS FROM RIGHT TO LEFT
# 3 command line args:
#   1. (In parenthesis) the message to be displayed
#   2. How the color of the text should be display: default (solid color) or flicker (changes between two colors)
#   3. The text scrolling speed: slow, medium, or fast
##################################################################################################################


import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

if(len(sys.argv) < 4):
    print('Needs 3 args: 1.message   2.color (default or flicker)   3.Text speed (slow, medium, or fast)')
    sys.exit(0)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=options)

blueColor = graphics.Color(0, 0, 255)
yellowColor = graphics.Color(255, 204, 0)

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont('./fonts/6x13.bdf')
currentColor = blueColor
if(sys.argv[2] == "flicker"):
    nextColor = yellowColor
elif(sys.argv[2] == "default"):
    nextColor = blueColor
else:
    print("Invalid color arg: options are default or flicker")
    sys.exit(0)

speed = ""
if(sys.argv[3] == "slow"):
    speed = 0.05
elif(sys.argv[3] == "medium"):
    speed = 0.03
elif(sys.argv[3] == "fast"):
    speed = 0.01
else:
    print("Invalid speed arg: options are slow, medium, or fast")
    sys.exit(0)

pos = offscreen_canvas.width
my_text = sys.argv[1]

try:
    print('Press CTRL-C to stop.')
    i = 0
    while True:
        offscreen_canvas.Clear()
        if(i % 25 == 0):
            tempColor = currentColor
            currentColor = nextColor
            nextColor = tempColor
        len = graphics.DrawText(offscreen_canvas, font, pos, 12, currentColor, my_text)
        pos -= 1

        # Entire message reached end of screen
        if(pos + len < 0):
            pos = offscreen_canvas.width
        if(i == 2000000):
            i = 1
        else:
            i += 1
        time.sleep(speed)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
except KeyboardInterrupt:
    sys.exit(0)
