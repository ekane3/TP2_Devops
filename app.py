import requests
import json
import os

from flask import Flask, render_template, request

api_key = os.environ.get('API_KEY')
app = Flask(__name__)

# create a function that returns the weather for a specific location using env lat and lon
def get_weather(lat, lon, api_key):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    return data

@app.route('/<lat>/<lon>')
def index(lat, lon, api_key ):
    weather = get_weather(lat, lon, api_key)
    #return render_template('index.html', weather=weather) #hh
    return "<p><b>Weather !</b></p><br><p>%s</p>" % weather

if __name__ == "__main__":
    #print(get_weather(lat, lon, api_key))
    app.run(debug=True)