import socket
import json

class UdpClient:
    def __init__(self, IP="127.0.0.1",port=5555):
        self.IP = IP
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, packet_id, data):
        packet = {
            "packet_id": packet_id,
            "data": data
        }
        json_string = json.dumps(packet)

        self.socket.sendto(json_string.encode('utf-8'), (self.IP, self.port))


    