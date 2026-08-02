from datetime import datetime
import time
import requests
import math

BASE_URL = "https://api.openf1.org/v1"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}



def sync_time(current_time_str, prev_time_obj):
    if current_time_str is None:
        return prev_time_obj

    current_time_obj = datetime.fromisoformat(current_time_str)

    if prev_time_obj is not None:
        delta = (current_time_obj - prev_time_obj).total_seconds()

        if delta > 0:
            time.sleep(delta)

    return current_time_obj

def fetch_api_data(endpoint, **parameters): # delego la raccolta da API alla funzione ausqiliaria insieme ai checks
    url = f"{BASE_URL}/{endpoint}"

    try: 
        response = requests.get(url, params=parameters, headers=HEADERS)

        if response.status_code == 401:
            print(f"Errore 401 sull'endpoint /{endpoint}: Sessione Live in corso. Riprova a fine gara!")
            return None

        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"Nessun dato trovato per l'endpoint /{endpoint}!")
            return None

        return data

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API (/{endpoint}): {e}")
        return None

def calculate_yaw(curr_x, curr_y, prev_x, prev_y):  # calcolo il vettore di rotazione per le vetture
    # YAW : arctan2(curr_y - prev_y, curr_x - prev_x) restituisce radianti, *(180/pi) restituisce gradi
    if prev_x is None or prev_y is None:
        return 0.0

    delta_x = curr_x - prev_x
    delta_y = curr_y - prev_y

    yaw = math.atan2(delta_y,delta_x)
    return math.degrees(yaw)