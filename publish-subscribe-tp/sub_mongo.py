import pymongo
import time

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mesures_env"]
collection = db["co2"]

print("En attente des nouvelles mesures CO2...")

dernier_id = None

try:
    while True:
        query = {}
        if dernier_id:
            query = {"_id": {"$gt": dernier_id}}
        nouveaux_docs = list(collection.find(query).sort("_id", 1))
        if nouveaux_docs:
            for doc in nouveaux_docs:
                date = doc.get("date")
                valeur = doc.get("valeur_de_CO2")
                print(f"Reçu - Date : {date}, Valeur CO2 : {valeur}")
            dernier_id = nouveaux_docs[-1]["_id"]

        time.sleep(1)  # Pause pour limiter le polling

except KeyboardInterrupt:
    print("Arrêt de la souscription par l'utilisateur.")
