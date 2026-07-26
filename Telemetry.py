import requests

def get_driver_laps(session_key, driver_number):
    url = "https://api.openf1.org/v1/laps"

    parameter = { "session_key": session_key, "driver_number": driver_number}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"\nRecupero i tempi per il pilota {driver_number} nella sessione {session_key}...")

    try:
        response = requests.get(url, params=parameter, headers=headers)

        if response.status_code == 401:
            print("\nErrore 401: Il server continua a bloccarci. Potrebbe essere necessario usare un'altra session_key.")
            print(f"Dettagli dal server: {response.text}")
            return

        response.raise_for_status()

        laps_data = response.json()

        if not laps_data:
            print(f"\nNessun dato trovato con questi parametri. Verifica l'ID sessione!")
            return

        print(f"\nTrovati {len(laps_data)} giri. Ecco i primi 5:\n")
        print("-" *50)

        for lap in laps_data[:5]:
            lap_number = lap.get("lap_number", "N/D")
            lap_seconds = lap.get("lap_duration","N/D")

            print(f"Giro: {lap_number} | Tempo: {lap_seconds} secondi")

        print("-" *50)
        print("Script completato con successo!")

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def search_max_speed(session_key, driver_number): 
    url = "https://api.openf1.org/v1/car_data"

    parameters = {"session_key": session_key, "driver_number": driver_number}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"\nAnalizzo la telemetria per il pilota {driver_number} nella sessione {session_key}...")

    try: 
        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        telemetry_data = response.json()

        if not telemetry_data:
            print("Nessun dato di telemetria!")
            return

        max_speed = 0
        peak_details = None

        for packet in telemetry_data:
            current_speed = packet.get("speed", 0)

            if current_speed > max_speed:
                max_speed = current_speed
                peak_details = packet

        print("-" *50)
        print(f"Velocità MASSIMA registrata: {max_speed} km/h")
        print("-" *50)
        print("Dettagli dell'auto in quel momento esatto:")
        print(f"1. Marcia inserita: {peak_details.get('n_gear')}")
        print(f"2. Giri motore (RPM): {peak_details.get('rpm')}")
        print(f"3. Acceleratore: {peak_details.get('throttle')}%")
        print(f"4. Freno premuto: {'Sì' if peak_details.get('brake') > 0 else 'No'}")
        print(f"• DRS Aperto: {'Sì' if peak_details.get('drs') in [10, 12, 14] else 'No'}")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

if __name__ == "__main__":
    get_driver_laps(session_key=9159, driver_number=55)
    search_max_speed(session_key=9159, driver_number=55)
