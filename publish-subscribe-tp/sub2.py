import redis
import time
from datetime import datetime
from collections import deque
import threading

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

pubsub = r.pubsub()
pubsub.subscribe('mesure_co2')

data_1min = deque()
data_30min = deque()
data_60min = deque()

def nettoyer_old_data(deque_obj, interval_sec):
    now = datetime.now()
    while deque_obj and (now - deque_obj[0][0]).total_seconds() > interval_sec:
        deque_obj.popleft()

def calculer_moyenne(deque_obj):
    if not deque_obj:
        return 0
    total = sum(val for _, val in deque_obj)
    return total / len(deque_obj)

def calcul_moyennes_periodique():
    while True:
        time.sleep(60)  # toutes les minutes
        nettoyer_old_data(data_1min, 60)
        nettoyer_old_data(data_30min, 1800)
        nettoyer_old_data(data_60min, 3600)
        moy_1min = calculer_moyenne(data_1min)
        moy_30min = calculer_moyenne(data_30min)
        moy_60min = calculer_moyenne(data_60min)
        print(f"Moyenne CO2 dernière minute : {moy_1min:.2f} ppm")
        print(f"Moyenne CO2 30 dernières minutes : {moy_30min:.2f} ppm")
        print(f"Moyenne CO2 dernière heure : {moy_60min:.2f} ppm\n")

threading.Thread(target=calcul_moyennes_periodique, daemon=True).start()

print("En attente des messages CO2...")

try:
    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            data = message['data']
            date_str, valeur_str = data.split(',')
            dt = datetime.fromisoformat(date_str)
            valeur = int(valeur_str)
            data_1min.append((dt, valeur))
            data_30min.append((dt, valeur))
            data_60min.append((dt, valeur))
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Arrêt du script par l'utilisateur.")
