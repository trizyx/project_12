import requests


class WeatherAPI:
    def __init__(self, base_url:str, apikey:str) -> None:
        self.base_url = base_url
        self.apikey = apikey

    def get_location_weather(self, location:str):
        url = f"{self.base_url}locations/v1/cities/search"
        try:
            query = {
            'apikey': self.apikey,
            'q': location,
            'language': 'en-us',
            'details': True,
            'toplevel':False,

        }
            response = requests.get(url=url, params=query)
            response.raise_for_status()
            location_data = response.json()
            if not location_data:
                raise ValueError(f"Нет результатов для локации: {location}")

            location_key = location_data[0]["Key"]
            return location_key

        except requests.exceptions.RequestException as e:
            print(f"Плохой запрос {e}")
            raise
        except (ValueError, IndexError) as e:
            print(f"Ошибка {e}")
            raise


    def get_location_weather(self, latitude:float, longitude:float):
        url = f"{self.base_url}locations/v1/cities/geoposition/search"
        try:
            query = {
            'apikey': self.apikey,
            'q': f'{latitude}, {longitude}',
            'language': 'en-us',
            'details': False,
            'toplevel':False,
        }
            response = requests.get(url=url, params=query)
            response.raise_for_status()
            location_data = response.json()
            if not location_data:
                raise ValueError(f"Нет результатов для локации: {latitude}, {longitude}")

            location_key = location_data[0]["Key"]
            return location_key

        except requests.exceptions.RequestException as e:
            print(f"Плохой запрос {e}")
            raise
        except (ValueError, IndexError) as e:
            print(f"Ошибка {e}")
            raise

        
    def get_weather(self, location_key:str):
        try:
            request_url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}'
            query = {
                'apikey': self.apikey,
                'language': 'en-us',
                'details': True,
                'metric': True,
            }
            response = requests.get(url=request_url, params=query)

            if response.status_code == 200:
                weather: dict = response.json()[0]
                temperature = weather.get('Temperature').get('Value')
                humidity = weather.get('RelativeHumidity')
                speed_wind = weather.get('Wind').get('Speed').get('Value')
                precipitation = weather.get("PrecipitationSummary").get("PastHour").get('Value')
                
                return {
                    'temperature': temperature, 
                    'humidity': humidity,
                    'wind_speed': speed_wind,
                    'precipitation': precipitation
                }

            raise f'{response.status_code} | {response.text}'
        except Exception as e:
            print(e)
            return None
