import pymongo
import time
import random
from datetime import datetime

# Connexion au serveur MongoDB local (ajuste si besoin)
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Choix de la base et de la collection
db = client["mesures_env"]
collection = db["co2"]

print("Publication des mesures CO2 dans MongoDB...")

while True:
    valeur_co2 = random.randint(400, 1000)  # mesure simulée
    date_now = datetime.now()

    document = {
        "date": date_now,
        "valeur_de_CO2": valeur_co2
    }

    collection.insert_one(document)
    print(f"Publié : {document}")

    # Pause entre 1 et 3 secondes
    time.sleep(random.uniform(1, 3))
