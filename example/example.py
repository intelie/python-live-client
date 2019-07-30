import cometd_live_client
from tcp_live_client import TcpClient


class PrintListener(cometd_live_client.AbstractListener):
    def __init__(self):
        super().__init__()

    def on_event(self, event):
        print(event)


class SendToLiveListener(cometd_live_client.AbstractListener):
    def __init__(self, ip, port):
        super().__init__()
        self.tcp_client = TcpClient('localhost', 17042)

    def on_event(self, event):
        self.tcp_client.send(event)


query1 = cometd_live_client.Query("=> random() as r1 every second")
query1.add_listener(PrintListener())
query1.add_listener(SendToLiveListener('localhost', 17042))

query2 = cometd_live_client.Query("=> random() as r2 every second")
query2.add_listener(PrintListener())

client = cometd_live_client.CometdClient(
    "http://localhost:8080", "admin", "admin", [query1, query2])

client.execute()
