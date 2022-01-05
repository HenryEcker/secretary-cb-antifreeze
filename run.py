import os
from datetime import datetime
from time import sleep

import chatexchange


def main(email, password, host_id, room_id, tries=3):
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
        # Join Room
        room.join()
        msg = f'{datetime.utcnow()}: Writer’s Block'
        # Send message
        room.send_message(msg)
    finally:
        # Leave and logout
        room.leave()
        client.logout()


if __name__ == '__main__':
    assert os.environ['SECRETARY_EMAIL']
    assert os.environ['SECRETARY_PASSWORD']
    assert os.environ['SECRETARY_ROOM_HOST']
    assert os.environ['SECRETARY_ROOM']
    main(
        email=os.environ['SECRETARY_EMAIL'],
        password=os.environ['SECRETARY_PASSWORD'],
        host_id=os.environ['SECRETARY_ROOM_HOST'],
        room_id=os.environ['SECRETARY_ROOM']
    )
