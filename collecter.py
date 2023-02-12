from datetime import datetime, timezone
import secret
from pyowm import OWM

import pickle


# CONSTANTS
Time = datetime.today().replace(microsecond=0)
#owm = pyowm.OWM()

# set owm api key
owm_apikey = None
if not owm_apikey:
    owm_apikey = secret.owm_apikey()

own_location_id = None
if not own_location_id:
    own_location_id = secret.own_location_id()


class api:
    def __init__(self) -> None:
        print("class api initiated")

    def data(self):
        # TODO
        # catch one api call and save it to a file for re-use (development)
        data = {}
        #owm = OWM(owm_apikey)
        #mgr = owm.weather_manager()
        #obs = mgr.weather_at_id(own_location_id)
        #w = obs.weather

        #with open("api_data.pkl", "wb") as f:
        #    pickle.dump(w, f)

        with open('api_data.pkl', 'rb') as f:
            w = pickle.load(f)

        sunrise_date = w.sunrise_time(timeformat='date')
        data['sunrise_date'] = sunrise_date
        sunrise_iso = w.sunrise_time(timeformat='iso')
        data['sunrise_iso'] = sunrise_iso
        return data

    def pretty_print(self):
        d = self.data()
        print("data:\n", d)
        print("date:", d['sunrise_date'])
        print("iso:", d['sunrise_iso'])



def start():
    print("Hej")
    a = api()
    #a.save_apicall()
    print(a.pretty_print())














if __name__ == "__main__":
    start()