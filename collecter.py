import sys
from datetime import datetime, timezone
import secret
from pyowm import OWM
import pytz
import pickle

# CONSTANTS
Time = datetime.today().replace(microsecond=0)

# set owm api key
owm_apikey = None
if not owm_apikey:
    owm_apikey = secret.owm_apikey()

own_location_id = None
if not own_location_id:
    own_location_id = secret.own_location_id()

# testing
online_call = False
store_to_file = True


class api:
    def __init__(self, store_db=False) -> None:
        self.data = {}
        self.sql_data = {}
        self.call_api()

        self.store_db = store_db
        if self.store_db:
            self.store_to_db()


    def call_api(self):

        w = None
        if online_call:
            try:
                owm = OWM(owm_apikey)
                mgr = owm.weather_manager()
                obs = mgr.weather_at_id(own_location_id)
                w = obs.weather
                if store_to_file:
                    with open("api_data.pkl", "wb") as f:
                        pickle.dump(w, f)
                else:
                    pass

            except Exception as E:
                print("No data from OWM. Error:", E)

        else:
            with open('api_data.pkl', 'rb') as f:
                w = pickle.load(f)

        if not w:
            print("No data form owm, exit code. (Add Yahoo weather or other service?)")
            sys.exit()

        self.data = w
        self.sql_data = self.sort_data(w)

    def sort_data(self, w: dict) -> dict:
        data = {}
        data['source'] = "Open Weather Map"
        if w.humidity:
            data['humidity'] = w.humidity
        if w.detailed_status:
            data['status'] = w.detailed_status

        if w.temperature(unit="fahrenheit")['temp']:
            tmp_f = w.temperature(unit="fahrenheit")['temp']
            convert = (float(tmp_f) - 32) * .5556
            data['temperature'] = round(convert, 2)

        if w.rain:
            if '1h' in w.rain():
                data['rain_1h'] = w.rain()['1h']
            if '3h' in w.rain():
                data['rain_3h'] = w.rain()['3h']
            else:
                data['rain_1h'] = w.rain()
        if w.snow:
            if '1h' in w.snow():
                data['snow_1h'] = w.snow()['1h']
            if '3h' in w.snow():
                data['snow_3h'] = w.snow()['3h']
            else:
                data['snow_1h'] = w.snow()
        if w.wind:
            data['wind_speed'] = w.wind()['speed']
            data['wind_deg'] = w.wind()['deg']
            if 'gust' in w.wind():
                data['wind_gust'] = w.wind()['gust']
            else:
                pass
        if w.clouds:
            data['clouds'] = w.clouds

        if w.sunrise_time('iso'):
            sunrise = w.sunrise_time('iso')
            data['sunrise'] = datetime.strptime(sunrise, '%Y-%m-%d %H:%M:%S+00:00')
            # data['sunrise'] = w.sunrise_time('iso')
        if w.sunset_time('iso'):
            sunset = w.sunset_time('iso')
            data['sunset'] = datetime.strptime(sunset, '%Y-%m-%d %H:%M:%S+00:00')
            # data['sunset'] = w.sunset_time('iso')
        if w.reference_time(timeformat='iso'):
            api_time = w.reference_time(timeformat='iso')
            data['api_time'] = datetime.strptime(api_time, '%Y-%m-%d %H:%M:%S+00:00')
            # data['api_time'] = w.reference_time(timeformat='iso')
        if data['temperature']:
            return data
        else:
            raise Exception("did not have a temperature value, discarding")

    def pretty_print(self):
        print("value : key : datatype")
        for x in self.sql_data:
            print(x, ":", self.sql_data[x], ":", type(self.sql_data[x]))

    def store_to_db(self):
        # TODO
        print("Initiate database store pls..")


def start():
    # initiate class
    #a = api(store_db=True)
    a = api(True)
    #a = api()
    print("Do a pretty print:")
    a.pretty_print()


if __name__ == "__main__":
    start()
