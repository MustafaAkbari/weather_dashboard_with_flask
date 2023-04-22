import requests
from configparser import ConfigParser
from flask import Flask, render_template, redirect, url_for, flash
from forms import WeatherForm


# creating a function that generate api key
def get_api_key():
    """
    to get apikey
    :return: apikey
    """
    config = ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api_key"]


# creating a function that get weather data from openweathermap
def get_weather_data(city_name, api_key):
    """
    To get weather data from openweathermap
    :param city_name: name of the city that we want to check for weather info
    :param api_key: apikey
    :return: weather info in the form of json
    """
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={api_key}"
    response = requests.get(api_url)
    return response.json()


# creating flask app
app = Flask(__name__)
# generate secret key
app.config["SECRET_KEY"] = "this is a weather data app"


# creating a route for home page
@app.route("/", methods=["GET", "POST"])
def home():
    form = WeatherForm()
    weather_data = None
    if form.validate_on_submit():
        weather_data = get_weather_data(form.city_name.data, get_api_key())
        return redirect(url_for("weather_result"), weather_data=weather_data)
    return render_template("home.html", form=form, weather_data=weather_data)


# creating a route for result page
@app.route("/result", methods=["POST"])
def weather_result():
    form = WeatherForm()
    city_name = form.city_name.data
    api_key = get_api_key()
    try:
        data = get_weather_data(city_name=city_name, api_key=api_key)
        weather_situation = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        location = data['name']
        return render_template("result.html", weather_situation=weather_situation, temperature=temperature,
                               location=location)
    except KeyError:
        flash(f"There is no city name like {city_name}", "warning")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
