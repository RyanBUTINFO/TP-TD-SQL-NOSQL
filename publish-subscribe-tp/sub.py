import time 
import random
import datetime
import json, copy, redis
import pandas as pd



r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe('mesure_co2')

print("En attente des messages CO2...")

try:
    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            data = message['data']
            print(f"Reçu: {data}")

except KeyboardInterrupt:
    print("Arrêt du script par l'utilisateur.")
