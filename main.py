import threading
from Network import UdpClient
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

    # Creazione threads
    telemetry_thread = threading.Thread(target=simulate_dashboard, args=(session,pilot,udp_client))
    position_thread = threading.Thread(target=simulate_location, args=(session,pilot,udp_client))
    weather_thread = threading.Thread(target=simulate_weather, args=(session,udp_client))
    intervals_thread = threading.Thread(target=simulate_intervals, args=(session, pilot,udp_client))
    laps_thread = threading.Thread(target=simulate_laps, args=(session, pilot,udp_client))
    race_control_thread = threading.Thread(target=simulate_race_control, args=(session,udp_client))
    leaderboard_thread = threading.Thread(target=simulate_leaderboard, args=(session,udp_client))
    radio_thread = threading.Thread(target=simulate_radio, args=(session,pilot,udp_client))

    # Setup non-threaded
    
    
    # get_driver_laps(session_key=session, driver_number=pilot)
    # search_max_speed(session_key=session, driver_number=pilot)
    # analyze_pit_stop(session_key=session, driver_number=pilot)
    # simulate_dashboard(session_key=session, driver_number=pilot)
    # simulate_location(session_key=session, driver_number=pilot)
    # analyze_weather(session_key=session)
    # telemetry_thread.start()
    # weather_thread.start()
    # intervals_thread.start()
    # laps_thread.start()
    # race_control_thread.start()
    # fetch_driver_info(session_key=session)
    # fetch_stints_info(session_key=session, driver_number=pilot)
    # leaderboard_thread.start()
    # fetch_session_info(session_key=session)
    radio_thread.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Programma terminato")