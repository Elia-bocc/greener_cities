import requests
import json
from datetime import datetime

API_KEY = "c59356581429ee7ba8be1ac1f713ae7e"

base_coord = (38.6864, -9.2286)
top_lat = 38.8092
right_lon = -9.0781
inc_lat = (top_lat-base_coord[0])/10
inc_lon = (right_lon-base_coord[1])/15
coordinates = []

for i in range(10):
    for j in range(15):
        new_coord = (base_coord[0]+i*inc_lat, base_coord[1]+j*inc_lon)
        coordinates.append(new_coord)



# Funzione per ottenere i dati di qualità dell'aria per ogni punto
def get_air_quality_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Funzione per generare il GeoJSON
def create_geojson():
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Per ogni coordinate, fai la richiesta all'API
    for lat, lon in coordinates:
        data = get_air_quality_data(lat, lon)

        # Estrai i dati
        aqi = data['list'][0]['main']['aqi']
        pm2_5 = data['list'][0]['components']['pm2_5']
        pm10 = data['list'][0]['components']['pm10']
        no2 = data['list'][0]['components']['no2']
        co = data['list'][0]['components']['co']
        o3 = data['list'][0]['components']['o3']
        timestamp = datetime.utcfromtimestamp(data['list'][0]['dt'])

        # Aggiungi ogni punto come una feature nel GeoJSON
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "pm2_5": pm2_5,
                "pm10": pm10,
                "no2": no2,
                "co": co,
                "o3": o3,
                "aqi": aqi,
                "timestamp": timestamp.isoformat()
            }
        }

        geojson_data["features"].append(feature)

    # Salva il file GeoJSON
    with open('air_pollution.geojson', 'w') as f:
        json.dump(geojson_data, f, indent=4)

    print("GeoJSON file created sucessfully!")

# Esegui la funzione per creare il file GeoJSON
create_geojson()
