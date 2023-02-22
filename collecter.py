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
    def __init__(self) -> None:
        self.data = {}
        self.sql_data = {}
        self.call_api()

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
            print("Yahoo weather?")

        print(w.humidity)
        self.data = w
        self.sql_data = self.sort_data(w)


    def sort_data(self, w: dict) -> dict:
        print("Hej")
        print(w.humidity)
        #print(w.values())
        d = {}
        return d


    def data(self):
        # TODO
        # catch one api call and save it to a file for re-use (development)
        w = self.data
        data = {}
        #try:
            # owm = OWM(owm_apikey)
            # mgr = owm.weather_manager()
            # obs = mgr.weather_at_id(own_location_id)
            # w = obs.weather

            # with open("api_data.pkl", "wb") as f:
            #    pickle.dump(w, f)

            #with open('api_data.pkl', 'rb') as f:
            #    w = pickle.load(f)

        #except Exception as E:
        #    print("No data from OWM. Error:", E)

        if not w:
            print("Yahoo weather?")

        #print(w.humidity)
        # print(w.)

        sunrise_date = w.sunrise_time(timeformat='date')
        data['sunrise_date'] = sunrise_date
        # sunrise_iso = w.sunrise_time(timeformat='iso')
        # sunrise_iso = w.sunrise_time(timeformat='iso', tzinfo='1')
        # data['sunrise_iso'] = sunrise_iso
        # sunrise = w.sunrise_time()
        # data['sunrise'] = sunrise

        # print("TEST:", w.humidity)

        return data

    def pretty_print(self):
        d = self.data
        print("data:\n", d)
        # print("date:", d['sunrise_date'], "type:", type(d['sunrise_date']))
        # print("iso:", d['sunrise_iso'], "type:", type(d['sunrise_iso']))
        # print("UNIX: data['sunrise']:", d['sunrise'], "type:", type(d['sunrise']))
        # print(datetime.utcfromtimestamp(d['sunrise']).strftime('%Y-%m-%d %H:%M:%S'))
        # convert_unix = datetime.utcfromtimestamp(d['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        # print("timenow():", Time.tzinfo)
        # local_tz = pytz.timezone('Europe/Stockholm')
        # time_test = d['sunrise']
        # time_test = time_test.replace(tzinfo=local_tz)
        # print("Works?:", time_test, convert_unix)

        # print((d['sunrise_date'].timezone.utc))


def start():
    print("Hej")
    a = api()
    # print(a.pretty_print())
    print(a.pretty_print())
    # print(api.data())


if __name__ == "__main__":
    start()
