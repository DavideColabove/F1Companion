import socket
import json
from Logger import logger

class UdpClient:
    def __init__(self, IP="127.0.0.1",port=5555):
        self.IP = IP
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.schemas = {
            "dashboard_data": {
            "speed": (int, float),
            "gear_number": int,
            "rpm": int,
            "throttle": int,
            "brake": (int, float),
            "drs": int,
            "timestamp": (str, type(None))
            },
            "radio_comms_data":{
                "recording_url": str,
                "timestamp": str
            },
            "weather_data":{
                "air_temp": (int, float),
                "track_temp": (int, float),
                "humidity": (int, float),
                "rainfall": (int, float),
                "timestamp": (str, type(None)),
                "wind_speed": (int, float),
                "wind_dir": (int, float),
                "pressure": (int, float)
            },
            "location_data":{
                "x_coordinate": (int, float),
                "y_coordinate": (int, float),
                "yaw": (int, float),
                "z_coordinate": (int, float),
                "timestamp": (str, type(None))              
            },
            "intervals_data": {
                "leader_gap": (int, float),
                "interval": (int, float),
                "timestamp":(str, type(None))
            },
            "laps_data": {
                "lap_number": int,
                "sec1": (int, float, str),
                "sec2": (int, float, str),
                "sec3": (int, float, str),
                "lap_duration": (int, float),
                "is_personal_best": bool,
                "timestamp": (str, type(None))
            },
            "race_control_data": {
                "category": (str, type(None)),
                "flag": (str, type(None)),
                "message": (str, type(None)),
                "timestamp": (str, type(None))
            },
            "leaderboard_data": {
                "driver_number": int,
                "position" : int,
                "timestamp": (str, type(None))
            },
            "session_info": {
                "circuit": (str, type(None)),
                "country": (str, type(None)),
                "session": (str, type(None)),
                "session_type": (str, type(None))
            },
            "driver_info": dict,
            "stints_info": dict,
        }

    def send_data(self, packet_id, data):
        if not self.validate_payload(packet_id, data):
            return
        
        packet = {
            "packet_id": packet_id,
            "data": data
        }
        json_string = json.dumps(packet)

        self.socket.sendto(json_string.encode('utf-8'), (self.IP, self.port))

    def validate_payload(self, packet_id, data):
        scheme = self.schemas.get(packet_id)

        if scheme is None:          # Temporaneo finche non definiamo tutti gli schemi
            return True

        if isinstance(scheme, type):
            if not isinstance(data, scheme):
                logger.warning(f"[SECURITY] Pacchetto '{packet_id}' SCARTATO. L'intero payload doveva essere di tipo {scheme}, ricevuto {type(data)}")
                return False
            return True

        for key, expected_type in scheme.items():
            value = data.get(key)
            if not isinstance(value,expected_type):
                logger.warning(f"[SECURITY] Pacchetto '{packet_id}' SCARTATO. Chiave '{key}' errata: {value} (Ricevuto: {type(value)}, Atteso: {expected_type})")
                return False 
        return True