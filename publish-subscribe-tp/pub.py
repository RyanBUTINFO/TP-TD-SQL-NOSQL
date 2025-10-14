import time 
import random
import datetime
import json, copy, redis
import pandas as pd

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

while True:
    valeur_co2 = random.randint(400, 1000)
    date_now = datetime.datetime.now()
    message = f"{date_now},{valeur_co2}"
    r.publish('mesure_co2', message)
    print(f"Published: {message}")
    time.sleep(random.uniform(1, 3))
