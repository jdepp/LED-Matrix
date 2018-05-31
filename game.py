import sys, os
import time
import signal
import random
from threading import Thread, Lock
import curses
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

# Setting up keyboard input library
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
font = graphics.Font()
font.LoadFont('./fonts/6x10.bdf')
matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()

# Colors
blue_color = graphics.Color(0, 0, 255)
white_color = graphics.Color(255, 255, 255)
red_color = graphics.Color(255, 0, 0)
green_color = graphics.Color(0, 255, 0)
purple_color = graphics.Color(128, 0, 128)
yellow_color = graphics.Color(255, 140, 0)
orange_color = graphics.Color(255, 70, 0)

colors = [blue_color, red_color, green_color, orange_color]

# Variables for the actual game
timer_number = 20
pick_ups = []
win = False
lock = Lock()


# Class that represents a single dot (a game pick up) on the matrix
class PickUp:
    def __init__(self, x_val, y_val, r, c):
        self.x = x_val
        self.y = y_val
        self.radius = r
        self.color = c


# Runs as a daemon thread that counts down from a certain number each second and renders the timer on the matrix
def timer(can):
    global timer_number
    global win
    while True:
        can.Clear()
        len = graphics.DrawText(can, font, can.width-12, 11, white_color, str(timer_number))
        render_pick_ups(can)
        graphics.DrawCircle(can, player_x, player_y, 0, blue_color)
        can = matrix.SwapOnVSync(can)
        time.sleep(1)
        timer_number -= 1
        if(timer_number <= 0):
            break
        if(win == True):
            break


# Function that creates the initial array of pick ups
def create_pick_ups():
    for idx in range(0, 10):
        x_pos = random.randint(2, 50)
        y_pos = random.randint(2, 13)
        while x_pos == 1 and y_pos == 1:
            x_pos = random.randint(2, 61)
            y_pos = random.randint(2, 13)
        pick_ups.append(PickUp(x_pos, y_pos, 0, yellow_color))


# Function that renders everything: the player, the pick ups, and the timer
def render_everything(can):
    can.Clear()
    len = graphics.DrawText(can, font, can.width - 12, 11, white_color, str(timer_number))
    render_pick_ups(can)
    graphics.DrawCircle(can, player_x, player_y, 0, blue_color)
    can = matrix.SwapOnVSync(can)


# Function that renders a message and displays it for 5 seconds
def render_message(canvas, message, color):
    global lock_timer
    lock_timer = True
    canvas.Clear()
    len = graphics.DrawText(canvas, font, 2, 11, color, message)
    canvas = matrix.SwapOnVSync(canvas)
    time.sleep(5)


# Function that renders all of the pick ups
def render_pick_ups(canvas):
    for pick_up in pick_ups:
        graphics.DrawCircle(canvas, pick_up.x, pick_up.y, pick_up.radius, pick_up.color)
    canvas = matrix.SwapOnVSync(canvas)


# Explodes the pick up when collected
def explode_pick_up(canvas, current_pick_up, current_pick_up_index):
    global win
    for idx in range(0, 4):
        current_pick_up.radius += 1
        current_pick_up.color = colors[idx%4]
        pick_ups[current_pick_up_index] = current_pick_up
        render_everything(canvas)
        time.sleep(.04)
    pick_ups.remove(current_pick_up)

    # If pick ups list is empty, player won
    if not pick_ups:
        win = True


# Function that quits keyboard input and then exits the whole program
def quit_program():
    curses.endwin()
    sys.exit(1)


# Main loop that starts the timer daemon thread and waits for user keyboard input
player_x = 1
player_y = 1
try:
    create_pick_ups()
    render_everything(canvas)
    graphics.DrawCircle(canvas, player_x, player_y, 0, blue_color)
    canvas = matrix.SwapOnVSync(canvas)
    timer_thread = Thread(target=timer, args=(canvas,))
    timer_thread.daemon = True
    timer_thread.start()
    key = ''
    while timer_thread.is_alive() == True:
        key = stdscr.getch()
        stdscr.addch(20,25,key)
        stdscr.refresh()
        check_boundry = 0
        canvas.Clear()
        if key == ord('w'):
            check_boundry = player_y
            check_boundry -= 1
            if(check_boundry >= 0):
                player_y -= 1
        elif key == ord('a'):
            check_boundry = player_x
            check_boundry -= 1
            if (check_boundry >= 0):
                player_x -= 1
        elif key == ord('d'):
            check_boundry = player_x
            check_boundry += 1
            if(check_boundry <= 50):
                player_x += 1
        elif key == ord('s'):
            check_boundry = player_y
            check_boundry += 1
            if(check_boundry <= 15):
                player_y += 1

        render_everything(canvas)

        # Checks if a user is on top of a pick up
        idx = 0
        for pick_up in pick_ups:
            if(player_x == pick_up.x and player_y == pick_up.y):
                render_pick_ups(canvas)
                graphics.DrawCircle(canvas, player_x, player_y, 0, blue_color)
                explode_pick_up_thread = Thread(target=explode_pick_up, args=(canvas, pick_up, idx))
                explode_pick_up_thread.daemon = True
                explode_pick_up_thread.start()
            idx += 1

    if(win == True):
        render_message(canvas, "You win!", blue_color)
    else:
        render_message(canvas, "Times up!", red_color)
    quit_program()


except KeyboardInterrupt:
    quit_program()
