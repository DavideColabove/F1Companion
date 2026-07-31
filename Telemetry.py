from datetime import datetime
import requests
import time
import sys

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

        print("\n") 
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

        print("\n")
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

        print("\n")
        print("-" *50)
        print(f"Dati PIT stop")
        print("-" *50)

        pit_stop_counter = len(pit_data)
        print(f"Il pilota ha effettuato {pit_stop_counter} pit stop.")


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

        print("-" *50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def simulate_dashboard(session_key, driver_number):
    url = "https://api.openf1.org/v1/car_data"

    parameters = {"session_key": session_key, "driver_number": driver_number}     

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Dashboard IRT")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        car_data = response.json()

        if not car_data:
            print("Nessun dato relativo alla velocità!")
            return

        prev_timestamp = None
        
        for packet in car_data:
            speed = packet.get("speed",0)
            gear_number = packet.get("n_gear",0)
            rpm = packet.get("rpm",0)
            throttle = packet.get("throttle",0)
            brake = packet.get("brake",0)
            timestamp = packet.get("date")

            if speed == 0 or timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                prev_timestamp = current_timestamp
                continue
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()
                                   
            dashboard_stream = f"| Velocità: {speed:3} km/h | Marcia: {gear_number} | RPM: {rpm} | Acceleratore: {throttle}% | Freno: {brake}% |"

            sys.stdout.write('\r' + dashboard_stream)
            sys.stdout.flush()

            time.sleep(timestamp_delta)

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
            print(f"Errore di comunicazione con le API: {e}")

def analyze_weather(session_key):
    url = "https://api.openf1.org/v1/weather"  

    parameters = {"session_key": session_key}     
    
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Condizioni METEO real-time")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        weather_data = response.json()

        if not weather_data:
            print("Nessun dato relativo al meteo!")
            return 

        max_temp = 0
        min_temp = float('inf')
        wet = False

        prev_timestamp = None

        for packet in weather_data:
            air_temp = packet.get("air_temperature", 0)
            track_temp = packet.get("track_temperature", 0)
            humidity = packet.get("humidity", 0)
            rainfall = packet.get("rainfall", 0)
            timestamp = packet.get("date")
            wind_speed = packet.get("wind_speed", 0)
            wind_dir = packet.get("wind_direction", 0)
            pressure = packet.get("pressure", 0)

            if timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                timestamp_delta = 0
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()

            if rainfall > 0:
                wet = True

            if track_temp:
                if track_temp > max_temp:
                    max_temp = track_temp
                if track_temp < min_temp:
                    min_temp = track_temp

            weather_stream = f"| Aria: {air_temp}°C | Asf: {track_temp}°C | Pioggia: {wet} | Vento: {wind_speed}m/s ({wind_dir}°) | Press: {pressure}mbar |"

            time.sleep(timestamp_delta)

            sys.stdout.write('\r' + weather_stream)
            sys.stdout.flush()

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
            print(f"Errore di comunicazione con le API: {e}")
        
def simulate_location(session_key, driver_number):
    url = "https://api.openf1.org/v1/location"

    parameters = {"session_key": session_key, "driver_number": driver_number}     

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Coordinate X,Y,Z")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        location_data = response.json()

        if not location_data:
            print("Nessun dato relativo alla posizione!")
            return

        prev_timestamp = None

        for packet in location_data:
            x_coordinate = packet.get("x")
            y_coordinate = packet.get("y")
            z_coordinate = packet.get("z")
            timestamp = packet.get("date")

            if x_coordinate == 0 or x_coordinate is None or timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                prev_timestamp = current_timestamp
                continue
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()

            location_stream = f"| Asse X: {x_coordinate:8.0f} | Asse Y: {y_coordinate:8.0f} | Asse Z: {z_coordinate:8.0f} |"

            sys.stdout.write('\r' + location_stream)
            sys.stdout.flush()

            time.sleep(timestamp_delta)

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def simulate_intervals(session_key, driver_number):
    url = "https://api.openf1.org/v1/intervals"

    parameters = {"session_key": session_key, "driver_number": driver_number}     
    
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Intervallo dal PRIMO e PRECEDENTE")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!") 
            return 

        response.raise_for_status()
        gaps_data = response.json()

        if not gaps_data:
            print("Nessun dato relativo agli intervalli!")
            return 

        prev_timestamp = None

        for packet in gaps_data:
            leader_gap = packet.get("gap_to_leader")
            interval = packet.get("interval")
            timestamp = packet.get("date")

            if leader_gap is None or interval is None or timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                prev_timestamp = current_timestamp
                continue
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()

            intervals_stream = f"| Gap Leader: +{leader_gap}s | Gap Precedente: +{interval}s |"

            sys.stdout.write('\r' + intervals_stream)
            sys.stdout.flush()

            time.sleep(timestamp_delta)

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def simulate_laps(session_key, driver_number):
    url = "https://api.openf1.org/v1/laps"

    parameters = {"session_key": session_key, "driver_number": driver_number}     

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Dati del GIRO")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        laps_data = response.json()

        if not laps_data:
            print("Nessun dato relativo ai giri!")
            return

        prev_timestamp = None

        for packet in laps_data:
            lap_number = packet.get("lap_number")
            sec1 = packet.get("duration_sector_1")
            sec2 = packet.get("duration_sector_2")
            sec3 = packet.get("duration_sector_3")
            lap_duration = packet.get("lap_duration")
            is_personal_best = packet.get("is_personal_best")
            timestamp = packet.get("date_start")

            if timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                timestamp_delta = 0
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()

            lap_duration = lap_duration if lap_duration is not None else "N/A"
            sec1 = sec1 if sec1 is not None else "N/A"
            sec2 = sec2 if sec2 is not None else "N/A"
            sec3 = sec3 if sec3 is not None else "N/A"

            pb_text = " (MIGLIOR GIRO PERSONALE!)" if is_personal_best else ""
            laps_stream = f"| Giro: {lap_number} | T1: {sec1} | T2: {sec2} | T3: {sec3} | Totale: {lap_duration}{pb_text} |"

            time.sleep(timestamp_delta)

            sys.stdout.write('\r' + laps_stream)
            sys.stdout.flush()

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def simulate_race_control(session_key):
    url = "https://api.openf1.org/v1/race_control"

    parameters = {"session_key": session_key}

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Informazioni di RACE CONTROL")
        print("-" *50)

        response = requests.get(url, params=parameters, headers= headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        race_control_data = response.json()

        if not race_control_data:
            print("Nessun dato relativo agli eventi di gara!")
            return

        prev_timestamp = None

        for packet in race_control_data:
            category = packet.get("category")
            flag = packet.get("flag")
            message = packet.get("message")
            timestamp = packet.get("date")

            if timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                timestamp_delta = 0
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()

            category = category if category is not None else "N/A"
            flag = flag if flag is not None else "N/A"
            message = message if message is not None else "N/A"

            race_control_stream = f"| [Race Control - {category}] Bandiera: {flag} | Trascrizione: {message} |"

            time.sleep(timestamp_delta)

            sys.stdout.write('\r' + race_control_stream)
            sys.stdout.flush()

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def fetch_driver_info(session_key):
    url = "https://api.openf1.org/v1/drivers"

    parameters = {"session_key": session_key}

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Informazioni sui PILOTI")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        driver_data = response.json()

        if not driver_data:
            print("Nessun dato relativo ai piloti!")
            return

        driver_registry = {}

        for packet in driver_data:
            driver_number = packet.get("driver_number")
            full_name = packet.get("full_name")
            name_acronym = packet.get("name_acronym")
            team_colour = packet.get("team_colour")

            if driver_number is None:
                continue

            if team_colour is not None:
                team_colour = f"#{team_colour}"
            else:
                team_colour = "#FFFFFF"

            driver_registry[driver_number] = { #dizionario
                "full_name": full_name,
                "name_acronym": name_acronym,
                "team_colour": team_colour
            }

            print(f"\nAuto: #{driver_number}| {name_acronym} | {full_name} | Colore: {team_colour} |")

        return driver_registry

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def fetch_stints_info(session_key, driver_number):
    url = "https://api.openf1.org/v1/stints"

    parameters = {"session_key": session_key, "driver_number": driver_number}

    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Informazioni GOMME")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        stints_data = response.json()

        if not stints_data:
            print("Nessun dato relativo agli eventi di gara!")
            return        

        stints_registry = {}

        for packet in stints_data:
            stint_number = packet.get("stint_number")
            compound = packet.get("compound")
            tyre_age_at_start = packet.get("tyre_age_at_start")
            lap_start = packet.get("lap_start")
            lap_end = packet.get("lap_end")

            if lap_start is None:
                continue

            if lap_end is not None:
                tyre_duration = lap_end - lap_start
            else:
                tyre_duration = "Fino a fine gara"

            stints_registry[lap_start] = { #dizionario per Unreal
                "compound": compound,
                "tyre_duration": tyre_duration,
                "tyre_age_at_start": tyre_age_at_start
            }

            print(f"\nNumero stint: #{stint_number}| Mescola: {compound} | Gomme usate: {tyre_age_at_start} | Giro iniziale: {lap_start} | Giro finale: {lap_end} |")

        return stints_registry

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

def simulate_leaderboard(session_key):
    url = "https://api.openf1.org/v1/position"

    parameters = {"session_key": session_key}

    headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

    try:
        print("\n")
        print("-" *50)
        print(f"Live LEADERBOARD")
        print("-" *50)

        response = requests.get(url, params=parameters, headers=headers)

        if response.status_code==401:
            print("Errore 401: Sessione Live in corso. Riprova a fine gara!")
            return

        response.raise_for_status()
        leaderboard_data = response.json()

        if not leaderboard_data:
            print("Nessun dato relativo alla leaderboard!")
            return

        prev_timestamp = None

        for packet in leaderboard_data:
            driver_number = packet.get("driver_number")
            position = packet.get("position")
            timestamp = packet.get("date")

            if timestamp is None:
                continue

            current_timestamp = datetime.fromisoformat(timestamp)

            if prev_timestamp is None:
                timestamp_delta = 0
            else:
                timestamp_delta = (current_timestamp - prev_timestamp).total_seconds()

            time.sleep(timestamp_delta)

            print(f"| [LEADERBOARD] Auto #{driver_number} è ora in P{position} |")

            prev_timestamp = current_timestamp

        print("-" *50)

    except requests.exceptions.RequestException as e:
            print(f"Errore di comunicazione con le API: {e}")