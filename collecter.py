from datetime import datetime
import secret


# CONSTANTS
Time = datetime.today().replace(microsecond=0)
#owm = pyowm.OWM()

# set owm api key
owm_apikey = None
if not owm_apikey:
    owm_apikey = secret.owm_apikey()


class api:
    def __init__(self) -> None:
        print("class api initiated")
        if self.data():
            print(self.data())
        else:
            print("No data to show")

    def data(self):
        print("return data pls")
        # TODO
        # catch one api call and save it to a file for re-use (development)
        data = {}
        return data



def start():
    print("Hej")
    api()














if __name__ == "__main__":
    start()