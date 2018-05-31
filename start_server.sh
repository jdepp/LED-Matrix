#!/usr/bin/env bash
# Sources
sudo python3 ./sources/spotify-server.py jdepp265 &
sudo python3 ./sources/weather-server.py &

# Main Server
sudo python3 ./show-spotify-song.py /tmp/spotify-current-song