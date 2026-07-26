import requests

def get_driver_laps(session_key, driver_number):
    url = "https://api.openf1.org/v1/laps"

    parameter = { "session_key": session_key, "driver_number": driver_number}

    print(f"\nRecupero i tempi per il pilota {driver_number} nella sessione {session_key}...")

    try:
        response = requests.get(url, params=parameter)
        response.raise_for_status()

        laps_data = response.json()

        if not laps_data:
            print(f"\nNessun dato trovato con questi parametri. Verifica l'ID sessione!")
            return

        print(f"\nTrovati {len(dati_giri)} giri. Ecco i primi 5:\n")
        print("-" *50)

        for lap in laps_data[:5]:
            lap_number = lap.get("lap_number", "N/D")
            lap_seconds = lap.get("lap_duration","N/D")

            print(f"Giro: {lap_number} | Tempo: {lap_seconds} secondi")

        print("-" *50)
        print("Script completato con successo!")

    except requests.exceptions.RequestException as e:
        print(f"Errore di comunicazione con le API: {e}")

if __name__ == "__main__":
    get_driver_laps(session_key= 9161, driver_number=63)