import logging
import os
from datetime import datetime
from time import sleep

from chatexchange.client import Client
from chatexchange.rooms import Room

logging.basicConfig(level=logging.DEBUG)


def main(
        email: str, password: str, host_id: str, room_id: str,
        tries: int = 3, retry_delay: int = 20, brief_delay: int = 2
) -> None:
    client: Client = Client(host_id)
    logging.info(f'Attempting to join Room {room_id} on "{host_id}"')

    attempt = 0
    while attempt < tries:
        client.login(email=email, password=password)
        attempt += 1
        if client.logged_in:
            logging.debug(f'Login attempt {attempt} failed.')
            break
        sleep(retry_delay)

    # Must be logged in at this point
    assert client.logged_in

    logging.info('Logged in')

    room: Room = client.get_room(room_id)
    try:
        # Join room
        room.join()
        logging.info('Joined Room')
        sleep(brief_delay)

        # Build and send message
        msg: str = f'{datetime.utcnow()}: Writer’s Block'
        room.send_message(msg)
        logging.info(f'Message written: ({msg})')
        sleep(brief_delay)
    finally:
        # logout
        client.logout()


if __name__ == '__main__':
    assert 'SECRETARY_EMAIL' in os.environ
    assert 'SECRETARY_PASSWORD' in os.environ
    assert 'SECRETARY_ROOM_HOST' in os.environ
    assert 'SECRETARY_ROOM' in os.environ
    main(
        email=os.environ.get('SECRETARY_EMAIL'),
        password=os.environ.get('SECRETARY_PASSWORD'),
        host_id=os.environ.get('SECRETARY_ROOM_HOST'),
        room_id=os.environ.get('SECRETARY_ROOM')
    )
