from Logger import logger
from datetime import datetime
import requests
import time
import sys
from Utils import (sync_time,
                   fetch_api_data,
                   calculate_yaw)

# Funzioni dati storici
def analyze_driver_laps(session_key, driver_number):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Dati GIRI")
    logger.info("-" *50)

    laps_data = fetch_api_data("laps", session_key=session_key, driver_number=driver_number)

    if not laps_data:
        logger.warning(f"Nessun dato trovato con questi parametri. Verifica l'ID sessione!")
        return

    logger.info("") 
    logger.info("-" *50)
    logger.info(f"Tempo PER giro")
    logger.info("-" *50)

    for lap in laps_data[:20]:
        lap_number = lap.get("lap_number", "N/D")
        lap_seconds = lap.get("lap_duration","N/D")

        logger.info(f"Giro: {lap_number} | Tempo: {lap_seconds} secondi")

    logger.info("-" *50)

def analyze_max_speed(session_key, driver_number): 
    logger.info("")
    logger.info("-" *50)
    logger.info(f"MAX Speed")
    logger.info("-" *50)

    telemetry_data = fetch_api_data("car_data", session_key=session_key, driver_number=driver_number)

    if not telemetry_data:
        logger.warning("Nessun dato di telemetria!")
        return

    max_speed = 0
    peak_details = None

    for packet in telemetry_data:
        current_speed = packet.get("speed", 0)

        if current_speed > max_speed:
            max_speed = current_speed
            peak_details = packet

    logger.info("")
    logger.info("-" *50)
    logger.info(f"Velocità MASSIMA registrata: {max_speed} km/h")
    logger.info("-" *50)
    logger.info("Dettagli dell'auto in quel momento esatto:")
    logger.info(f"1. Marcia inserita: {peak_details.get('n_gear')}")
    logger.info(f"2. Giri motore (RPM): {peak_details.get('rpm')}")
    logger.info(f"3. Acceleratore: {peak_details.get('throttle')}%")
    logger.info(f"4. Freno premuto: {'Sì' if peak_details.get('brake') > 0 else 'No'}")
    logger.info(f"5. DRS Aperto: {'Sì' if peak_details.get('drs') in [10, 12, 14] else 'No'}")
    logger.info("-" * 50)

def analyze_pit_stop(session_key, driver_number):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Dati PIT")
    logger.info("-" *50)

    pit_data = fetch_api_data("pit", session_key=session_key, driver_number=driver_number)

    if not pit_data:
        logger.warning("Nessun dato relativo ai pit stop!")
        return

    logger.info("")
    logger.info("-" *50)
    logger.info(f"Dati PIT stop")
    logger.info("-" *50)

    pit_stop_counter = len(pit_data)
    logger.info(f"Il pilota ha effettuato {pit_stop_counter} pit stop.")


    fastest_pit = float('inf')
    for packet in pit_data:
        current = packet.get("pit_duration") 
        if current is not None:
            if current < fastest_pit:
                fastest_pit = current

    if fastest_pit == float('inf'):
        logger.warning("Nessun tempo valido registrato per i pit stop.")
    else:
        logger.info(f"Il pit stop più veloce è durato {fastest_pit} secondi.")

    logger.info("-" *50)

# Funzioni non-Threaded
def fetch_driver_info(session_key):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Informazioni sui PILOTI")
    logger.info("-" *50)

    driver_data = fetch_api_data("drivers", session_key=session_key)

    if not driver_data:
        logger.warning("Nessun dato relativo ai piloti!")
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

        logger.info(f"Auto: #{driver_number}| {name_acronym} | {full_name} | Colore: {team_colour} |")

    return driver_registry

def fetch_stints_info(session_key, driver_number):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Informazioni GOMME")
    logger.info("-" *50)

    stints_data = fetch_api_data("stints", session_key=session_key, driver_number=driver_number)

    if not stints_data:
        logger.warning("Nessun dato relativo agli eventi di gara!")
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

        logger.info(f"Numero stint: #{stint_number}| Mescola: {compound} | Gomme usate: {tyre_age_at_start} | Giro iniziale: {lap_start} | Giro finale: {lap_end} |")

    return stints_registry

def fetch_session_info(session_key):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Informazioni sul CIRCUITO")
    logger.info("-" *50)

    session_data = fetch_api_data("sessions", session_key = session_key)

    if not session_data:
        logger.warning("Nessun dato relativo alla sessione!")
        return

    packet = session_data[0]

    circuit = packet.get("circuit_short_name", "N/A")
    country = packet.get("country_name", "N/A")
    session = packet.get("session_name", "N/A")
    session_type = packet.get("session_type", "N/A")

    session_registry = {
        "circuit": circuit,
        "country": country,
        "session": session,
        "session_type": session_type
    }

    logger.info(f"| Circuito: {circuit} ({country}) | Sessione: {session} | Tipo: {session_type} |")
    logger.info("-" *50)

    return session_registry

# Funzioni Threaded
def simulate_radio(session_key, driver_number, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Live RADIO")
    logger.info("-" *50)

    radio_data = fetch_api_data("team_radio", session_key=session_key, driver_number=driver_number)

    if not radio_data:
        logger.warning("Nessun dato relativo alle comunicazioni radio!")
        return

    prev_timestamp = None

    for packet in radio_data:
        recording_url = packet.get("recording_url")
        timestamp = packet.get("date")

        if timestamp is None:
            continue

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        radio_packet ={
            "recording_url": recording_url,
            "timestamp": timestamp
        }

        udp_client.send_data("radio_comms_data", radio_packet)

        logger.info(f"| Timestamp {timestamp} | Recording URL {recording_url} |")
        
    logger.info("-" *50)

def simulate_dashboard(session_key, driver_number, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Dashboard IRT")
    logger.info("-" *50)

    car_data = fetch_api_data("car_data", session_key=session_key, driver_number=driver_number)

    if not car_data:
        logger.warning("Nessun dato relativo alla velocità!")
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

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        dashboard_packet ={
            "speed": speed,
            "gear_number": gear_number,
            "rpm": rpm,
            "throttle": throttle,
            "brake": brake,
            "timestamp": timestamp
        }

        udp_client.send_data("dashboard_data", dashboard_packet)
                                
        dashboard_stream = f"| Velocità: {speed:3} km/h | Marcia: {gear_number} | RPM: {rpm} | Acceleratore: {throttle}% | Freno: {brake}% |"

        sys.stdout.write('\r' + dashboard_stream)
        sys.stdout.flush()

    logger.info("-" *50)

def simulate_weather(session_key, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Condizioni METEO real-time")
    logger.info("-" *50)

    weather_data = fetch_api_data("weather", session_key=session_key)

    if not weather_data:
        logger.warning("Nessun dato relativo al meteo!")
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

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        if rainfall > 0:
            wet = True

        if track_temp:
            if track_temp > max_temp:
                max_temp = track_temp
            if track_temp < min_temp:
                min_temp = track_temp

        weather_packet = {
            "air_temp": air_temp,
            "track_temp": track_temp,
            "humidity": humidity,
            "rainfall": rainfall,
            "timestamp": timestamp,
            "wind_speed": wind_speed,
            "wind_dir": wind_dir,
            "pressure": pressure
        }

        udp_client.send_data("weather_data", weather_packet)

        weather_stream = f"| Aria: {air_temp}°C | Asf: {track_temp}°C | Pioggia: {wet} | Vento: {wind_speed}m/s ({wind_dir}°) | Press: {pressure}mbar |"

        sys.stdout.write('\r' + weather_stream)
        sys.stdout.flush()

    logger.info("-" *50)

def simulate_location(session_key, driver_number, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Coordinate X,Y,Z")
    logger.info("-" *50)

    location_data = fetch_api_data("location", session_key=session_key, driver_number=driver_number)

    if not location_data:
        logger.warning("Nessun dato relativo alla posizione!")
        return

    prev_timestamp = None

    prev_y = None   # Necessari per calculare YAW
    prev_x = None

    for packet in location_data:
        x_coordinate = packet.get("x")
        y_coordinate = packet.get("y")
        yaw = calculate_yaw(x_coordinate, y_coordinate, prev_x, prev_y)
        z_coordinate = packet.get("z")
        timestamp = packet.get("date")

        if x_coordinate == 0 or x_coordinate is None or timestamp is None:
            continue

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        location_packet = {
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
            "yaw": yaw,
            "z_coordinate": z_coordinate,
            "timestamp": timestamp
        }

        udp_client.send_data("location_data", location_packet)

        location_stream = f"| Asse X: {x_coordinate:8.0f} | Asse Y: {y_coordinate:8.0f} | Asse Z: {z_coordinate:8.0f} | YAW: {yaw:7.2f}° |"

        sys.stdout.write('\r' + location_stream)
        sys.stdout.flush()

        prev_x = x_coordinate
        prev_y = y_coordinate

    logger.info("-" *50)

def simulate_intervals(session_key, driver_number, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Intervallo dal PRIMO e PRECEDENTE")
    logger.info("-" *50)

    gaps_data = fetch_api_data("intervals", session_key=session_key, driver_number=driver_number)

    if not gaps_data:
        logger.warning("Nessun dato relativo agli intervalli!")
        return 

    prev_timestamp = None

    for packet in gaps_data:
        leader_gap = packet.get("gap_to_leader")
        interval = packet.get("interval")
        timestamp = packet.get("date")

        if leader_gap is None or interval is None or timestamp is None:
            continue

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        intervals_packet = {
            "leader_gap": leader_gap,
            "interval": interval,
            "timestamp":timestamp
        }

        udp_client.send_data("intervals_data", intervals_packet)

        intervals_stream = f"| Gap Leader: +{leader_gap}s | Gap Precedente: +{interval}s |"

        sys.stdout.write('\r' + intervals_stream)
        sys.stdout.flush()

    logger.info("-" *50)

def simulate_laps(session_key, driver_number, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Dati del GIRO")
    logger.info("-" *50)

    
    laps_data = fetch_api_data("laps", session_key=session_key, driver_number = driver_number)

    if not laps_data:
        logger.warning("Nessun dato relativo ai giri!")
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

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        lap_duration = lap_duration if lap_duration is not None else "N/A"
        sec1 = sec1 if sec1 is not None else "N/A"
        sec2 = sec2 if sec2 is not None else "N/A"
        sec3 = sec3 if sec3 is not None else "N/A"

        laps_packet = {
            "lap_number": lap_number,
            "sec1": sec1,
            "sec2": sec2,
            "sec3": sec3,
            "lap_duration": lap_duration,
            "is_personal_best": is_personal_best,
            "timestamp": timestamp
        }

        udp_client.send_data("laps_data", laps_packet)

        pb_text = " (MIGLIOR GIRO PERSONALE!)" if is_personal_best else ""
        laps_stream = f"| Giro: {lap_number} | T1: {sec1} | T2: {sec2} | T3: {sec3} | Totale: {lap_duration}{pb_text} |"

        sys.stdout.write('\r' + laps_stream)
        sys.stdout.flush()

    logger.info("-" *50)

def simulate_race_control(session_key, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Informazioni di RACE CONTROL")
    logger.info("-" *50)

    race_control_data = fetch_api_data("race_control", session_key=session_key)

    if not race_control_data:
        logger.warning("Nessun dato relativo agli eventi di gara!")
        return

    prev_timestamp = None

    for packet in race_control_data:
        category = packet.get("category")
        flag = packet.get("flag")
        message = packet.get("message")
        timestamp = packet.get("date")

        if timestamp is None:
            continue

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        category = category if category is not None else "N/A"
        flag = flag if flag is not None else "N/A"
        message = message if message is not None else "N/A"

        race_control_packet = {
            "category": category,
            "flag": flag,
            "message": message,
            "timestamp": timestamp
        }

        udp_client.send_data("race_control_data", race_control_packet)

        race_control_stream = f"| [Race Control - {category}] Bandiera: {flag} | Trascrizione: {message} |"

        sys.stdout.write('\r' + race_control_stream)
        sys.stdout.flush()

    logger.info("-" *50)

def simulate_leaderboard(session_key, udp_client):
    logger.info("")
    logger.info("-" *50)
    logger.info(f"Live LEADERBOARD")
    logger.info("-" *50)

    leaderboard_data = fetch_api_data("position", session_key=session_key)

    if not leaderboard_data:
        logger.warning("Nessun dato relativo alla leaderboard!")
        return

    prev_timestamp = None

    for packet in leaderboard_data:
        driver_number = packet.get("driver_number")
        position = packet.get("position")
        timestamp = packet.get("date")

        if timestamp is None:
            continue

        prev_timestamp = sync_time(timestamp, prev_timestamp)

        leaderboard_packet = {
            "driver_number": driver_number,
            "position" : position,
            "timestamp": timestamp
        }

        udp_client.send_data("leaderboard_data", leaderboard_packet)

        logger.info(f"| [LEADERBOARD] Auto #{driver_number} è ora in P{position} |")

    logger.info("-" *50)
