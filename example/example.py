from liveclient import LiveClient, Query, AbstractListener

class PrintListener(AbstractListener):
    def __init__(self):
        super().__init__()

    def on_event(self, event):
        print(event)


class SendToLiveListener(AbstractListener):
    def __init__(self, tcp_client):
        super().__init__()
        self.tcp_client = tcp_client

    def on_event(self, event):
        self.tcp_client.send(event)

live_client = LiveClient("config.json")

query1 = Query("=> random() as r1 every second")
query1.add_listener(PrintListener())
query1.add_listener(SendToLiveListener(live_client.tcp_client))

query2 = Query("=> random() as r2 every second")
query2.add_listener(PrintListener())

cometd_live_client = live_client.cometd_client
cometd_live_client.add_queries([query1, query2])
cometd_live_client.execute()
