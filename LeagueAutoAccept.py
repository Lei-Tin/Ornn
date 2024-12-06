from lcu_driver import Connector
import asyncio

connector = Connector()


@connector.ready
async def connect(connection):
    print('LCU API attached.')


@connector.ws.register('/lol-matchmaking/v1/search', event_types=('CREATE',))
async def icon_changed(connection, event):
    print('Matchmaking start event received')


@connector.ws.register('/lol-matchmaking/v1/ready-check', event_types=('CREATE', 'UPDATE'))
async def icon_changed(connection, event):
    print('Matchmaking ready check event created')
    await asyncio.sleep(1)

    await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')
    print('Accept matchmaking')


if __name__ == '__main__':
    connector.start()
