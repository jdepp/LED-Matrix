import requests
import time
from xml.etree import ElementTree
# api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=5d828247d61c0e4d3bb35dc1e30f3fde&q=Boston'
# json_data = requests.get(api_address).json()
# #print(json_data)
# formatted_data= json_data['main']['temp']
# #tree= ElementTree.fromstring(xml_data.content)
# #print(formatted_data)

# Taking the json data and creating a xml file format
# Writing the temp of city to text file


def create_xml():
    api_address = 'https://api.darksky.net/forecast/755623129527d6300029b8343f569d0c/40.4406,79.9959'
    #api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=5d828247d61c0e4d3bb35dc1e30f3fde&q=Pittsburgh'
    json_data = requests.get(api_address).json()
    #deg_f = str(round(((json_data['main']['temp'] - 273.15) * 1.8) + 32))
    # message += deg_f + "°F        "
    # message += json_data['weather'][0]['description']
    # message += "</message>"
    weather_temp = str(round(json_data["hourly"]["data"][0]["temperature"]))
    weather_description = json_data["hourly"]["data"][0]["summary"]
    weather_msg = str("Weather in Pittsburgh: " + weather_temp + "F - " + weather_description)
    with open('/tmp/current-weather', 'w+') as file:
        contents = file.read().split("\n")
        file.seek(0)
        file.truncate()
        file.write(weather_msg)
    time.sleep(600)


while True:
    create_xml()