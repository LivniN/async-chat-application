import asyncio
import collections
from datetime import datetime

from app.server.context import log, config

Client = collections.namedtuple('Client', 'name client_time writer reader')
datetime_fmt = '%Y-%m-%d %H:%M:%S'


class ChatServer:
    def __init__(self, ip, port, loop):
        self.writers = dict()
        self.ip = ip
        self.port = port
        self.timeout = int(config['server']['client_timeout'])
        self.loop = loop

    async def chat_server(self):
        await asyncio.start_server(self.register, host=self.ip, port=self.port)
        log.info(f'Serving on {(self.ip, self.port)}')

    async def handle_client(self, client):
        try:
            while True:
                data = await asyncio.wait_for(client.reader.read(100), timeout=self.timeout)
                if not data:
                    log.info(f"{client.name} closed the connection.")
                    break
                message = data.decode().strip()
                log.info(f'got: {message} from {client.name}')
                client_time, msg, recipients = self.resolve_message_time_recipients(message)
                await self.send_message(client, client_time, msg, recipients)
                if msg == "exit":
                    message = f"{client.name} is disconnecting."
                    log.info(message)
                    await self.send_message(client, client_time, message)
                    break
        except asyncio.TimeoutError:
            log.warn(f"{client.name} reached timeout, disconnecting")
            client.writer.write('Bye!'.encode())
            await client.writer.drain()
        finally:
            client.writer.close()
            await client.writer.wait_closed()
            self.writers.pop(client.name)

    async def register(self, reader, writer):
        register_msg = await reader.read(100)
        client_time, client_name = register_msg.decode().strip().split(',')
        client = Client(name=client_name, client_time=client_time, writer=writer,
                        reader=reader)
        message = f"joined the chat"
        self.writers[client.name] = client
        await self.send_message(client, client_time, message)
        await self.handle_client(client)

    async def send_message(self, client, client_time, msg, recipients=dict()):
        pretty_time = datetime.utcfromtimestamp(int(client_time.split('.')[0])).strftime(datetime_fmt)
        for client_name, client_data in recipients.items() or self.writers.items():
            log.info(f"sending: {msg} to: {client_name}")
            client_data.writer.write(f"{pretty_time},{client.name}: {msg}".encode())
            await client_data.writer.drain()

    def resolve_message_time_recipients(self, message):
        splitted = message.split('@')
        client_time, msg = splitted[0].split(',')
        recipients_from_client = splitted[1:]
        recipients = dict()
        for client_name, client_data in self.writers.items():
            if client_name in recipients_from_client:
                recipients[client_name] = client_data
        return client_time, msg, recipients
