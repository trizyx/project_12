from flask import Flask, render_template, request
from get_weather import WeatherAPI
from weather_model import WeatherModel

app = Flask(__name__)
weather_api = WeatherAPI(base_url="http://dataservice.accuweather.com/", apikey='eZHywb5UeeyzNUTQWFYfqttT347QkoHg')
weather_model = WeatherModel()


@app.route("/", methods=["GET", "POST"])
def index():
    weather_condition = None
    error_message = None
    if request.method == "POST":
        search_type = request.form.get("search_type")
        city_name = request.form.get("city_name")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        try:
            if search_type == "city_name" and city_name:
                location_key = weather_api.get_location_weather(city_name)
            elif search_type == "coordinates" and latitude and longitude:
                location_key = weather_api.get_location_weather_coords(float(latitude), float(longitude))
            else:
                raise ValueError("Invalid input. Please provide a valid city name or coordinates.")

            weather_data = weather_api.get_weather(location_key)

            if weather_data:
                weather_condition = weather_model.check_bad_weather(
                    temperature=weather_data["temperature"],
                    windspeed=weather_data["wind_speed"],
                    humidity=weather_data["humidity"]
                )
            else:
                raise ValueError("Weather data is unavailable.")

        except Exception as e:
            error_message = str(e)

    return render_template("index.html", weather_condition=weather_condition, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)
