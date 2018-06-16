import time
import sys
import json
import re

import serial
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 2
options.parallel = 1
options.brightness = 80
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=options)

# Setting up colors
redColor = graphics.Color(255, 0, 0)
yellowColor = graphics.Color(255, 140, 0)
orangeColor = graphics.Color(255, 70, 0)
blueColor = graphics.Color(0, 0, 255)
greenColor = graphics.Color(0, 255, 0)
purpleColor = graphics.Color(128, 0, 128)
whiteColor = graphics.Color(255, 255, 255)
colors = [redColor, yellowColor, orangeColor, blueColor, greenColor, purpleColor, whiteColor]

canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont('./fonts/6x13.bdf')

serialport = serial.Serial("/dev/serial/by-id/usb-Arduino_LLC_Kano_sensor-if00", 9600)

radius = 0
leftX = 31
rightX = 32

print("Ctrl+C to exit")
try:
    while True:
        command = serialport.readline()
        command = command.decode('utf-8')
        numberList = re.findall(r'\d+', command)
        number = int(numberList[0])

        if(number < 8):
            radius = 1
            leftX = 31
            rightX = 32
        elif (number < 16):
            radius = 2
            leftX = 30
            rightX = 33
        elif (number < 24):
            radius = 3
            leftX = 29
            rightX = 34
        elif (number < 32):
            radius = 4
            leftX = 28
            rightX = 35
        elif (number < 40):
            radius = 5
            leftX = 27
            rightX = 36
        elif (number < 48):
            radius = 6
            leftX = 26
            rightX = 37
        elif (number < 56):
            radius = 7
            leftX = 25
            rightX = 38
        elif (number < 64):
            radius = 8
            leftX = 24
            rightX = 39
        elif (number < 72):
            radius = 9
            leftX = 23
            rightX = 40
        elif (number < 80):
            radius = 9
            leftX = 22
            rightX = 41
        elif (number < 88):
            radius = 9
            leftX = 21
            rightX = 42
        elif (number < 96):
            radius = 9
            leftX = 20
            rightX = 43
        elif (number < 104):
            radius = 9
            leftX = 19
            rightX = 44
        elif (number < 112):
            radius = 9
            leftX = 18
            rightX = 45
        elif (number < 120):
            radius = 9
            leftX = 17
            rightX = 46
        elif (number < 128):
            radius = 9
            leftX = 16
            rightX = 47
        elif (number < 136):
            radius = 9
            leftX = 15
            rightX = 48
        elif (number < 144):
            radius = 9
            leftX = 14
            rightX = 49
        elif (number < 152):
            radius = 9
            leftX = 13
            rightX = 50
        elif (number < 160):
            radius = 9
            leftX = 12
            rightX = 51
        elif (number < 168):
            radius = 9
            leftX = 11
            rightX = 52
        elif (number < 176):
            radius = 9
            leftX = 10
            rightX = 53
        elif (number < 184):
            radius = 9
            leftX = 9
            rightX = 54
        elif (number < 192):
            radius = 9
            leftX = 8
            rightX = 55
        elif (number < 200):
            radius = 9
            leftX = 7
            rightX = 56
        elif (number < 208):
            radius = 9
            leftX = 6
            rightX = 57
        elif (number < 216):
            radius = 9
            leftX = 5
            rightX = 58
        elif (number < 224):
            radius = 9
            leftX = 4
            rightX = 59
        elif (number < 232):
            radius = 9
            leftX = 3
            rightX = 60
        elif (number < 240):
            radius = 9
            leftX = 2
            rightX = 61
        elif (number < 248):
            radius = 9
            leftX = 1
            rightX = 62
        elif (number < 256):
            radius = 9
            leftX = 0
            rightX = 63
        else:
            radius = 10
            leftX = 32
            rightX = 32

        canvas.Clear()
        #graphics.DrawCircle(canvas, 32, 8, radius, blueColor)
        graphics.DrawLine(canvas, leftX, 0, rightX, 0, colors[0])
        graphics.DrawLine(canvas, leftX, 1, rightX, 1, colors[1])
        graphics.DrawLine(canvas, leftX, 2, rightX, 2, colors[2])
        graphics.DrawLine(canvas, leftX, 3, rightX, 3, colors[3])
        graphics.DrawLine(canvas, leftX, 4, rightX, 4, colors[4])
        graphics.DrawLine(canvas, leftX, 5, rightX, 5, colors[5])
        graphics.DrawLine(canvas, leftX, 6, rightX, 6, colors[6])
        graphics.DrawLine(canvas, leftX, 7, rightX, 7, colors[0])
        graphics.DrawLine(canvas, leftX, 8, rightX, 8, colors[1])
        graphics.DrawLine(canvas, leftX, 9, rightX, 9, colors[2])
        graphics.DrawLine(canvas, leftX, 10, rightX, 10, colors[3])
        graphics.DrawLine(canvas, leftX, 11, rightX, 11, colors[4])
        graphics.DrawLine(canvas, leftX, 12, rightX, 12, colors[5])
        graphics.DrawLine(canvas, leftX, 13, rightX, 13, colors[6])
        graphics.DrawLine(canvas, leftX, 14, rightX, 14, colors[0])
        graphics.DrawLine(canvas, leftX, 15, rightX, 15, colors[1])
        canvas = matrix.SwapOnVSync(canvas)

except KeyboardInterrupt:
    sys.exit(0)
