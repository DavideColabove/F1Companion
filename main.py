from Telemetry import (
    get_driver_laps, 
    search_max_speed, 
    analyze_pit_stop, 
    simulate_dashboard, 
    analyze_weather
)

def main():
    session = 9159
    pilot = 55
    
    get_driver_laps(session_key=session, driver_number=pilot)
    search_max_speed(session_key=session, driver_number=pilot)
    analyze_pit_stop(session_key=session, driver_number=pilot)
    simulate_dashboard(session_key=session, driver_number=pilot)
    # analyze_weather(session_key=sessione)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Programma terminato")