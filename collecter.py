from datetime import datetime
import secret


# CONSTANTS
Time = datetime.today().replace(microsecond=0)
#owm = pyowm.OWM()

# set owm api key
owm_apikey = None
if not owm_apikey:
    owm_apikey = secret.owm_apikey()




def start():
    print("Hej")














if __name__ == "__main__":
    start()