import threading
from Telemetry import (
    get_driver_laps, 
    search_max_speed, 
    analyze_pit_stop, 
    simulate_dashboard, 
    analyze_weather,
    simulate_location
)

def main():
    session = 9159
    pilot = 55

    telemetry_thread = threading.Thread(target=simulate_dashboard, args=(session,pilot))
    position_thread = threading.Thread(target=simulate_location, args=(session,pilot))
    weather_thread = threading.Thread(target=analyze_weather, args=(session,))
    
    get_driver_laps(session_key=session, driver_number=pilot)
    search_max_speed(session_key=session, driver_number=pilot)
    analyze_pit_stop(session_key=session, driver_number=pilot)
    # simulate_dashboard(session_key=session, driver_number=pilot)
    # simulate_location(session_key=session, driver_number=pilot)
    # analyze_weather(session_key=session)
    telemetry_thread.start()
    position_thread.start()
    weather_thread.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Programma terminato")