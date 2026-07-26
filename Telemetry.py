import requests

def get_driver_laps(session_key, driver_number):
    url = "https://api.openf1.org/v1/laps"

    parameter = { "session_key": session_key, "driver_number": driver_number}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

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

        print("-" *50)
        print(f"Tempo PER giro")
        print("-" *50)

        for lap in laps_data[:20]:
            lap_number = lap.get("lap_number", "N/D")
            lap_seconds = lap.get("lap_duration","N/D")

            print(f"Giro: {lap_number} | Tempo: {lap_seconds} secondi")

        print("-" *50)


    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def search_max_speed(session_key, driver_number): 
    url = "https://api.openf1.org/v1/car_data"

    parameters = {"session_key": session_key, "driver_number": driver_number}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

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
        print(f"5. DRS Aperto: {'Sì' if peak_details.get('drs') in [10, 12, 14] else 'No'}")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def analyze_pit_stop(session_key, driver_number):
    url = "https://api.openf1.org/v1/pit"
    
    parameters = {"session_key": session_key, "driver_number": driver_number}
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    try: 
        response = requests.get(url, params=parameters, headers=headers)
    
        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return
    
        response.raise_for_status()
        pit_data = response.json()
    
        if not pit_data:
            print("Nessun dato relativo ai pit stop!")
            return

        print("-" *50)
        print(f"Dati PIT stop")
        print("-" *50)

        pit_stop_counter = len(pit_data)
        print(f"\nIl pilota ha effettuato {pit_stop_counter} pit stop.")


        fastest_pit = float('inf')
        for packet in pit_data:
            current = packet.get("pit_duration") 
            if current is not None:
                if current < fastest_pit:
                    fastest_pit = current

        if fastest_pit == float('inf'):
            print("Nessun tempo valido registrato per i pit stop.")
        else:
            print(f"Il pit stop più veloce è durato {fastest_pit} secondi.")

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

        

if __name__ == "__main__":
    print(f"\nAnalizzo i dati per il pilota {55} nella sessione {9159}...")
    get_driver_laps(session_key=9159, driver_number=55)
    search_max_speed(session_key=9159, driver_number=55)
    analyze_pit_stop(session_key=9159, driver_number=55)
