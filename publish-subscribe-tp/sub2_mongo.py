import pymongo
import time
from datetime import datetime, timedelta

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mesures_env"]
collection = db["co2"]

def moyenne_co2(depuis):
    pipeline = [
        {"$match": {"date": {"$gte": depuis}}},
        {"$group": {"_id": None, "moyenne": {"$avg": "$valeur_de_CO2"}}}
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        return result[0]["moyenne"]
    return 0

print("Calcul des moyennes des valeurs CO2...")

try:
    while True:
        maintenant = datetime.now()
        debut_1min = maintenant - timedelta(minutes=1)
        debut_30min = maintenant - timedelta(minutes=30)
        debut_60min = maintenant - timedelta(hours=1)

        moy_1min = moyenne_co2(debut_1min)
        moy_30min = moyenne_co2(debut_30min)
        moy_60min = moyenne_co2(debut_60min)

        print(f"Moyenne CO2 dernière minute : {moy_1min:.2f} ppm")
        print(f"Moyenne CO2 30 dernières minutes : {moy_30min:.2f} ppm")
        print(f"Moyenne CO2 dernière heure : {moy_60min:.2f} ppm\n")

        time.sleep(60)

except KeyboardInterrupt:
    print("Arrêt du script par l'utilisateur.")
