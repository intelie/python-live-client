import sys
from abc import ABC, abstractmethod
import requests
import asyncio
from aiocometd import Client
from typing import List


class AbstractListener(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_event(self, event):
        pass


class Query:
    def __init__(self, expression, provider="pipes", realtime=True, preload=False, span="None"):
        self.query = {
            'provider': provider,
            'preload': preload,
            'span': span,
            'follow': realtime,
            'expression': expression
        }
        self.listeners = []

    def add_listener(self, listener: AbstractListener):
        self.listeners.append(listener)


QueryList = List[Query]


class CometdClient:
    def __init__(self, server, user, password, queries: QueryList = []):
        self.server = server
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.queries = queries

    def __request_payload(self):
        payload = []
        for query in self.queries:
            payload.append(query.query)
        return payload

    def __get_channels(self):
        request = self.session.post(
            self.server + "/rest/query", json=self.__request_payload())
        request.raise_for_status()
        channels = [
            item.get('channel')
            for item in request.json()
        ]
        return channels

    async def __subscribe_and_run(self):
        channels = self.__get_channels()
        channels_dict = dict(zip(channels, self.queries))

        # connect to the server
        async with Client(self.server + "/cometd") as client:
            for channel in channels:
                # subscribe to channel to receive events
                await client.subscribe(channel)
            async for message in client:
                query = channels_dict[message['channel']]
                data = message["data"]
                for listener in query.listeners:
                    listener.on_event(data)

    def add_queries(self, queries: QueryList = []):
        self.queries.extend(queries)

    def execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__subscribe_and_run())
