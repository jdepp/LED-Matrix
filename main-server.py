import time
import sys
import datetime
import pytz
from pytz import timezone
import os.path
from os import path

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image


source_files = [
    '/tmp/spotify-current-song',
    '/tmp/current-weather'
]


def display_datetime(canvas):
    current_datetime = datetime.datetime.now()
    current_datetime = current_datetime.astimezone(timezone('US/Eastern'))
    month = str(current_datetime.month)
    day = str(current_datetime.day)
    year = str(current_datetime.year)
    hour = current_datetime.hour
    if(hour > 12):
        hour -= 12
    hour = str(hour)
    minute = str(current_datetime.minute)
    if(len(minute) == 1):
        minute = "0" + minute
    time_string = hour + ":" + minute
    datetime_string = month + "/" + day + "/" + year + " - " + time_string
    # display_scrolling_text(canvas, datetime_string, white_color)
    font.LoadFont('./fonts/9x15.bdf')
    display_static_text(canvas, time_string, white_color)
    time.sleep(3)
    font.LoadFont('./fonts/6x13.bdf')


def display_weather(canvas, weather_info):
    display_scrolling_text(canvas, weather_info, blue_color)
    time.sleep(1)


def display_song(canvas, song_info):
    song_info_split = song_info.split(';')
    song_title = song_info_split[0]
    song_artist = song_info_split[len(song_info_split) - 1]

    pos = scroll_text_to_end(canvas, song_title, green_color)
    scroll_text_down(canvas, song_title, pos, green_color)

    scroll_text_to_end(canvas, song_artist, gray_color)
    canvas.Clear()
    time.sleep(1.2)


def scroll_text_to_end(canvas, text_to_be_displayed, color):
    x_pos = 2
    canvas.Clear()
    len = graphics.DrawText(canvas, font, x_pos, 12, color, text_to_be_displayed)
    canvas = matrix.SwapOnVSync(canvas)
    time.sleep(1)
    while True:
        canvas.Clear()
        len = graphics.DrawText(canvas, font, x_pos, 12, color, text_to_be_displayed)
        canvas = matrix.SwapOnVSync(canvas)
        x_pos -= 1
        if (x_pos + len < 63):
            #pos = canvas.width
            x_pos += 1
            time.sleep(1)
            break
        time.sleep(0.02)

    return x_pos


def scroll_text_down(canvas, text_to_be_displayed, x_pos, color):
    vert_pos = 12
    while True:
        canvas.Clear()
        len = graphics.DrawText(canvas, font, x_pos, vert_pos, color, text_to_be_displayed)
        time.sleep(0.03)
        vert_pos += 1
        if (vert_pos >= 28):
            time.sleep(0.3)
            break
        canvas = matrix.SwapOnVSync(canvas)


def display_static_text(canvas, text_to_be_displayed, color):
    len = graphics.DrawText(canvas, font, 1, 12, color, text_to_be_displayed)
    canvas = matrix.SwapOnVSync(canvas)


def display_scrolling_text(canvas, text_to_be_displayed, color):
    pos = canvas.width
    while True:
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, 12, color, text_to_be_displayed)
        pos -= 1
        if (pos + len < 0):
            pos = canvas.width
            break
        time.sleep(0.02)
        canvas = matrix.SwapOnVSync(canvas)


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

blue_color = graphics.Color(0, 0, 255)
red_color = graphics.Color(255, 0, 0)
yellow_color = graphics.Color(255, 204, 0)
green_color = graphics.Color(0, 255, 0)
purple_color = graphics.Color(127, 0, 255)
white_color = graphics.Color(255, 255, 255)
gray_color = graphics.Color(190, 190, 190)


offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont('./fonts/6x13.bdf')
#pos = offscreen_canvas.width
current_text = ""

try:
    i = 0
    print('Press CTRL-C to stop.')
    while True:
        if(path.isfile(source_files[i])):
            file_to_be_read = open(source_files[i], 'r')
            items_array = [line.strip() for line in file_to_be_read.readlines()]

            # Reading from current song playing file -> display current song
            if(i == 0):
                for item in items_array:
                    display_song(offscreen_canvas, item)

            # Reading from current weather file -> display current weather
            elif(i == 1):
                for item in items_array:
                    display_weather(offscreen_canvas, item)

            i += 1

            if(i == 2):
                display_datetime(offscreen_canvas)
                i = 0


except KeyboardInterrupt:
    sys.exit(0)