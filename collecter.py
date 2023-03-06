import sys
import pymysql
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
online_call = True
store_to_file = False
old_db = True


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
                text = "No data from OWM. Error:" + str(E)
                self.write_log(text)

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
        try:
            h, u, p, db, t = secret.sql()
            columns = []
            values = []
            for x in self.sql_data:
                columns.append(x)
                values.append(self.sql_data[x])

            database = pymysql.connect(host=h, user=u, password=p, db=db)
            sql_string = 'INSERT INTO ' + t + ' (' + ', '.join(columns) + ') VALUES (' + (
                    '%s, ' * (len(columns) - 1)) + '%s)'

            cursor = database.cursor()
            cursor.execute(sql_string, tuple(values))
            database.commit()
            database.close()
            # also supply the older database
            if old_db:
                h, u, p, db = secret.old_sql()
                database = pymysql.connect(host=h, user=u, password=p, db=db)
                cursor = database.cursor()
                values = (str(self.sql_data['temperature']), str(self.sql_data['humidity']),
                          str(self.sql_data['status']), Time)
                cursor.execute(secret.old_sql_query(), values)
                database.commit()
                database.close()

        except pymysql.Error as e:
            text = "Error saving to DB: " + str(e)
            self.write_log(text)

    def write_log(self, text: str):
        try:
            f_name = "log_y" + str(datetime.now().strftime("%Y")) + "_w" + str(datetime.now().strftime("%W")) + ".txt"
            f = open(secret.log_dir() + f_name, "a")
            ts = datetime.today().replace(microsecond=0)
            text = "[" + str(ts) + "] " + text + "\n"
            f.write(str(text))
            f.close()

        except Exception as e:
            print("Could not write log: " + str(e))
            print("Tried to log: ", text)
            pass


def start():
    # initiate class
    a = api(store_db=True)
    # print("Do a pretty print:")
    #a.pretty_print()


if __name__ == "__main__":
    start()
