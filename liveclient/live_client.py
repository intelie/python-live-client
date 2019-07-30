import json
from liveclient.tcp_live_client import TcpClient
from liveclient.cometd_live_client import CometdClient


class LiveClient:
    def __init__(self, config_file_name):
        with open(config_file_name) as config_file:
            config = json.load(config_file)
            self.tcp_client = TcpClient(
                config['tcp']['ip'], config['tcp']['port'])
            self.cometd_client = CometdClient(
                config['cometd']['host'], config['cometd']['user'], config['cometd']['password'])
