from pyowm import OWM
from geopy import Nominatim
import datetime
import weatherstack
from googletrans import Translator

class Weather:
    # location of the weather
    __location = "Springfield, US"

    # API Key
    api_key = "6b0a6f6a62dff7712f2c44394f17270b"

    def __init__(self):
        self.ws = weatherstack.Client(self.api_key)
        locator = Nominatim(user_agent="geo")
        city = "Springfield"
        country = "United States"
        self.__location = city + "," + country
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude

    @property
    def weather(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        historical_today = self.ws.historical(
            lat=self.lat,
            lon=self.long,
            start_date=today,
            end_date=today,
            hourly=True
        )
        historical_tomorrow = self.ws.historical(
            lat=self.lat,
            lon=self.long,
            start_date=tomorrow,
            end_date=tomorrow,
            hourly=True
        )
        return historical_today, historical_tomorrow

my_weather = Weather()
print(my_weather.weather)
