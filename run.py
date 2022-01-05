import os
from datetime import datetime
from time import sleep

import chatexchange


def main(email, password, host_id, room_id, tries=3):
    print(repr(host_id), repr(room_id))
    exit(0)
    client = chatexchange.client.Client(host_id)

    attempt = 0
    while attempt < tries:
        client.login(email=email, password=password)
        attempt += 1
        if client.logged_in:
            break
        sleep(20)

    # Must be logged in at this point
    assert client.logged_in

    room = client.get_room(room_id)
    try:
        msg = f'{datetime.utcnow()}: Writer’s Block'
        # Send message
        room.send_message(msg)
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
