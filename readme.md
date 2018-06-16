# LED Matrix

An LED Matrix that displays information such as currently playing song on Spotify, the current weather and time, and really any information that can be obtained by a public API.
The purpose of this project is for fun and to learn a bit about hardware, python, and Raspberry Pi.

The start_server shell script starts the necessary APIs as well as the main server to display the information.

## Additional Functionality
* Motion Sensor: implemented [Kano's Motion Sensor](https://kano.me/store/us/products/motion-sensor-kit) to perform animations on the LED matrix. The sensor detects motion and writes JSON data to a serial port on the Pi which can be used to in a Python script using the open source Github repo [PySerial](https://github.com/pyserial/pyserial).
* Simple game: a game that uses the 'w', 'a', 's', and 'd' keys to move a dot (the player) around to pick up various pickups before time runs out. Uses the Python library Curses to detect user input.
* Explosion animation: an animation of different colored circles that start small and grow until a certain radius and then disapear. Meant to simulate fireworks.

## Hardware Used

* Raspberry Pi 3B [linked here](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* Adafruit Hat to control the LED Matrix [linked here](https://www.adafruit.com/product/2345)
* Two LED 16x32 pixel Matrices [linked here](https://www.adafruit.com/product/420)
* 5V 4A power supply [linked here](https://www.adafruit.com/product/1466)
* Kano Motion Sensor Kit [linked here](https://kano.me/store/us/products/motion-sensor-kit)

## Content Sources
The project currently has two API sources:
 * Music - Spotify
 * Weather - Dark Skies API



#### Author
Jeremy Deppen

