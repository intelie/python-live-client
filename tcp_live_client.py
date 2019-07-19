import json
import socket
import logging

class TcpClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send(self, event):
        message = '{}\n'.format(json.dumps(event))
        message = bytes(message, 'utf-8')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.ip, self.port))
            sock.sendall(message)
        except socket.error:
            logging.exception("ERROR: Cannot send event, server unavailable")
            logging.exception("Event data: {}".format(message))
        finally:
            sock.close()
