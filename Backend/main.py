import threading
import time
from Network import UdpClient
from Logger import logger
from Telemetry import (
    analyze_driver_laps, 
    analyze_max_speed, 
    analyze_pit_stop, 
    simulate_dashboard, 
    simulate_weather,
    simulate_location,
    simulate_intervals,
    simulate_laps,
    simulate_race_control,
    simulate_leaderboard,
    simulate_radio,
    fetch_driver_info,
    fetch_stints_info,
    fetch_session_info,
)

def main():
    session = 9165
    pilot = 1

    udp_client = UdpClient()

    # Setup non-threaded
    driver_registry = fetch_driver_info(session_key=session)
    udp_client.send_data("driver_info", driver_registry)

    session_registry = fetch_session_info(session_key=session)
    udp_client.send_data("session_info", session_registry)

    stints_registry = fetch_stints_info(session_key=session, driver_number=pilot)
    udp_client.send_data("stints_info", stints_registry)

    # Creazione threads
    telemetry_thread = threading.Thread(target=simulate_dashboard, args=(session,pilot,udp_client))
    position_thread = threading.Thread(target=simulate_location, args=(session,pilot,udp_client))
    weather_thread = threading.Thread(target=simulate_weather, args=(session,udp_client))
    intervals_thread = threading.Thread(target=simulate_intervals, args=(session, pilot,udp_client))
    laps_thread = threading.Thread(target=simulate_laps, args=(session, pilot,udp_client))
    race_control_thread = threading.Thread(target=simulate_race_control, args=(session,udp_client))
    leaderboard_thread = threading.Thread(target=simulate_leaderboard, args=(session,udp_client))
    radio_thread = threading.Thread(target=simulate_radio, args=(session,pilot,udp_client))

    telemetry_thread.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Programma terminato")