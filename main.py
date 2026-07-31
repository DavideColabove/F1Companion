import threading
from Telemetry import (
    get_driver_laps, 
    search_max_speed, 
    analyze_pit_stop, 
    simulate_dashboard, 
    analyze_weather,
    simulate_location,
    simulate_intervals,
    simulate_laps,
    simulate_race_control,
    fetch_driver_info,
    fetch_stints_info
)

def main():
    session = 9165
    pilot = 1

    telemetry_thread = threading.Thread(target=simulate_dashboard, args=(session,pilot))
    position_thread = threading.Thread(target=simulate_location, args=(session,pilot))
    weather_thread = threading.Thread(target=analyze_weather, args=(session,))
    intervals_thread = threading.Thread(target=simulate_intervals, args=(session, pilot))
    laps_thread = threading.Thread(target=simulate_laps, args=(session, pilot))
    race_control_thread = threading.Thread(target=simulate_race_control, args=(session,))
    
    
    # get_driver_laps(session_key=session, driver_number=pilot)
    # search_max_speed(session_key=session, driver_number=pilot)
    # analyze_pit_stop(session_key=session, driver_number=pilot)
    # simulate_dashboard(session_key=session, driver_number=pilot)
    # simulate_location(session_key=session, driver_number=pilot)
    # analyze_weather(session_key=session)
    # telemetry_thread.start()
    # position_thread.start()
    # weather_thread.start()
    # intervals_thread.start()
    # laps_thread.start()
    # race_control_thread.start()
    # fetch_driver_info(session_key=session)
    fetch_stints_info(session_key=session, driver_number=pilot)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Programma terminato")