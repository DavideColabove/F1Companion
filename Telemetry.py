<<<<<<< HEAD
import fastf1
import time
import sys

# FastF1 salva i dati in cache per evitare di riscaricali ogni volta
fastf1.Cache.enable_cache("f1_cache")


def load_session(year, grand_prix, session_type="R"):
    print(f"\nCaricamento sessione: {grand_prix} {year} - {session_type}...")
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()
    print("Sessione caricata con successo.")
    return session


def get_driver_pos(session, driver_abbr):
    print("\n")
    print("-" * 50)
    print(f"Risultato finale - {driver_abbr}")
    print("-" * 50)

    results = session.results
    driver_result = results[results["Abbreviation"] == driver_abbr]

    if driver_result.empty:
        print(f"Nessun risultato trovato per {driver_abbr}.")
        print("-" * 50)
        return

    row = driver_result.iloc[0]
    status = row["Status"]
    classified_pos = str(row["ClassifiedPosition"])
    grid_pos = row["GridPosition"]

    print(f"Partenza dalla posizione: P{int(grid_pos)}")

    if classified_pos == "R":
        print(f"Risultato:               DNF (Ritirato)")
        print(f"Motivo:                  {status}")
    elif classified_pos == "W":
        print(f"Risultato:               DNS (Non partito)")
        print(f"Motivo:                  {status}")
    elif classified_pos == "D" or classified_pos == "E":
        print(f"Risultato:               DSQ (Squalificato)")
        print(f"Motivo:                  {status}")
    elif classified_pos == "N":
        print(f"Risultato:               NC (Non classificato)")
        print(f"Status:                  {status}")
    else:
        try:
            pos = int(float(classified_pos))
            print(f"Posizione finale:        P{pos}")
            print(f"Status:                  {status}")
        except (ValueError, TypeError):
            print(f"Risultato:               {classified_pos}")
            print(f"Status:                  {status}")

    print("-" * 50)


def get_driver_laps(session, driver_abbr):
    print("\n")
    print("-" * 50)
    print(f"Tempo PER giro - {driver_abbr}")
    print("-" * 50)

    laps = session.laps.pick_drivers(driver_abbr)

    if laps.empty:
        print(f"Nessun dato trovato per il pilota {driver_abbr}.")
        return

    for _, lap in laps.iterrows():
        lap_number = lap["LapNumber"]
        lap_time = lap["LapTime"]

        if lap_time is None or (hasattr(lap_time, "isnull") and lap_time.isnull()):
            continue

        # Converti timedelta in secondi
        lap_seconds = round(lap_time.total_seconds(), 3)
        print(f"Giro: {int(lap_number):>2} | Tempo: {lap_seconds} secondi")

    print("-" * 50)


def search_max_speed(session, driver_abbr):
    print("\n")
    print("-" * 50)
    print(f"Velocita' MASSIMA - {driver_abbr}")
    print("-" * 50)

    laps = session.laps.pick_drivers(driver_abbr).pick_fastest()

    if laps is None:
        print(f"Nessun giro veloce trovato per {driver_abbr}.")
        return

    car_data = laps.get_car_data()

    if car_data.empty:
        print("Nessun dato di telemetria disponibile.")
        return

    max_speed_idx = car_data["Speed"].idxmax()
    peak = car_data.loc[max_speed_idx]
    max_speed = peak["Speed"]

    print(f"Velocita' MASSIMA registrata: {max_speed:.1f} km/h")
    print("-" * 50)
    print("Dettagli dell'auto in quel momento esatto:")
    print(f"1. Marcia inserita:   {int(peak['nGear'])}")
    print(f"2. Giri motore (RPM): {int(peak['RPM'])}")
    print(f"3. Acceleratore:      {int(peak['Throttle'])}%")
    print(f"4. Freno premuto:     {'Si' if peak['Brake'] else 'No'}")
    print(f"5. DRS Aperto:        {'Si' if peak['DRS'] in [10, 12, 14] else 'No'}")
    print("-" * 50)


def analyze_pit_stop(session, driver_abbr):
    print("\n")
    print("-" * 50)
    print(f"Dati PIT stop - {driver_abbr}")
    print("-" * 50)

    laps = session.laps.pick_drivers(driver_abbr).reset_index(drop=True)

    # Giri con entrata ai box
    pit_in_laps = laps[laps["PitInTime"].notna()]

    if pit_in_laps.empty:
        print(f"Nessun pit stop trovato per il pilota {driver_abbr}.")
        return

    print(f"Il pilota ha effettuato {len(pit_in_laps)} pit stop.")

    fastest_pit = None
    for idx in pit_in_laps.index:
        pit_in = laps.loc[idx, "PitInTime"]
        # PitOutTime e' sul giro successivo
        next_idx = idx + 1
        if next_idx in laps.index:
            pit_out = laps.loc[next_idx, "PitOutTime"]
            if pit_out is not None and not (hasattr(pit_out, "isnull") and pit_out.isnull()):
                try:
                    duration = round((pit_out - pit_in).total_seconds(), 3)
                    if fastest_pit is None or duration < fastest_pit:
                        fastest_pit = duration
                except Exception:
                    continue

    if fastest_pit is not None:
        print(f"Il pit stop piu' veloce e' durato {fastest_pit} secondi.")
    else:
        print("Nessun tempo valido registrato per i pit stop.")

    print("-" * 50)


def simulate_dashboard(session, driver_abbr):

    print("\n")
    print("-" * 50)
    print(f"Dashboard IRT - {driver_abbr}")
    print("-" * 50)

    fastest_lap = session.laps.pick_drivers(driver_abbr).pick_fastest()

    if fastest_lap is None:
        print(f"Nessun giro veloce trovato per {driver_abbr}.")
        return

    car_data = fastest_lap.get_car_data()

    if car_data.empty:
        print("Nessun dato di telemetria disponibile.")
        return

    for _, packet in car_data.iterrows():
        speed = packet.get("Speed", 0)
        if speed == 0:
            continue
        gear = packet.get("nGear", 0)
        rpm = packet.get("RPM", 0)
        throttle = packet.get("Throttle", 0)
        brake = packet.get("Brake", 0)
        brake_str = "Si" if brake else "No"

        dashboard_stream = (
            f"| Velocita': {speed:6.1f} km/h | Marcia: {int(gear)} | "
            f"RPM: {int(rpm):>5} | Acceleratore: {int(throttle):>3}% | Freno: {brake_str} |"
        )

        sys.stdout.write("\r" + dashboard_stream)
        sys.stdout.flush()
        time.sleep(0.05)  # piu' veloce perche' i dati sono gia' locali

    print("\n" + "-" * 50)


def analyze_weather(session):
    """
    Mostra le condizioni meteo durante la sessione.
    """
    print("\n")
    print("-" * 50)
    print("Condizioni METEO della sessione")
    print("-" * 50)

    weather_data = session.weather_data

    if weather_data is None or weather_data.empty:
        print("Nessun dato meteo disponibile.")
        return

    max_track_temp = weather_data["TrackTemp"].max()
    min_track_temp = weather_data["TrackTemp"].min()
    avg_air_temp = weather_data["AirTemp"].mean()
    avg_humidity = weather_data["Humidity"].mean()
    wet = weather_data["Rainfall"].any()

    print(f"Temperatura aria media:    {avg_air_temp:.1f}C")
    print(f"Temperatura asfalto max:   {max_track_temp:.1f}C")
    print(f"Temperatura asfalto min:   {min_track_temp:.1f}C")
    print(f"Umidita' media:            {avg_humidity:.1f}%")
    print(f"Presenza pioggia:          {'Si' if wet else 'No'}")
    print("-" * 50)


if __name__ == "__main__":
    # === CONFIGURA QUI LA SESSIONE ===
    YEAR = 2026
    GRAND_PRIX = "Hungaroring"    # Nome del GP (es. "Monaco", "Monza", "Silverstone")
    SESSION_TYPE = "R"            # 'R'=Gara, 'Q'=Qualifiche, 'FP1'/'FP2'/'FP3'=Prove
    DRIVER = "LEC"                # Abbreviazione pilota (es. "VER", "HAM", "LEC", "SAI")
    # =================================

    session = load_session(YEAR, GRAND_PRIX, SESSION_TYPE)

    print(f"\nAnalizzo i dati per il pilota {DRIVER}...")
    get_driver_pos(session, DRIVER)
    get_driver_laps(session, DRIVER)
    search_max_speed(session, DRIVER)
    analyze_pit_stop(session, DRIVER)
    simulate_dashboard(session, DRIVER)
    #analyze_weather(session)
=======
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
        
        for packet in car_data:
            speed = packet.get("speed",0)
            if speed==0:
                continue
            gear_number = packet.get("n_gear",0)
            rpm = packet.get("rpm",0)
            throttle = packet.get("throttle",0)
            brake = packet.get("brake",0)

            dashboard_stream = f"| Velocità: {speed:3} km/h | Marcia: {gear_number} | RPM: {rpm} | Acceleratore: {throttle}% | Freno: {brake}% |"

            sys.stdout.write('\r' + dashboard_stream)
            sys.stdout.flush()

            time.sleep(0.27)

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

        for packet in weather_data:
            air_temp = packet.get("air_temperature", 0)
            track_temp = packet.get("track_temperature", 0)
            humidity = packet.get("humidity", 0)
            rainfall = packet.get("rainfall", 0)

            if rainfall > 0:
                wet = True

            if track_temp:
                if track_temp > max_temp:
                    max_temp = track_temp
                if track_temp < min_temp:
                    min_temp = track_temp

            weather_stream = f"| Temperatura aria: {air_temp}°C | Temperatura asfalto: {track_temp}°C | Umidità : {humidity}% | Pioggia: {wet} |"

            sys.stdout.write('\r' + weather_stream)
            sys.stdout.flush()
            
            time.sleep(0.5)

        print("-" *50)

    except requests.exceptions.RequestException as e:
            print(f"Errore di comunicazione con le API: {e}")
        



if __name__ == "__main__":
    print(f"\nAnalizzo i dati per il pilota {55} nella sessione {9159}...")
    get_driver_laps(session_key=9159, driver_number=55)
    search_max_speed(session_key=9159, driver_number=55)
    analyze_pit_stop(session_key=9159, driver_number=55)
    #simulate_dashboard(session_key=9159, driver_number=55)
    analyze_weather(session_key=9159)

>>>>>>> 743fee43a43c5e9b7ab2d3c06fecdb959c8d13df
