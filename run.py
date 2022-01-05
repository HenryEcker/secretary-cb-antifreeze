import os
from datetime import datetime
from time import sleep

import chatexchange


def main(email, password, host_id, room_id, tries=3):
    client = chatexchange.client.Client(host_id)

    attempt = 0
    while attempt < tries:
        try:
            client.login(email=email, password=password)
        except chatexchange.browser.LoginError:
            attempt += 1
            sleep(20)
        break

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
