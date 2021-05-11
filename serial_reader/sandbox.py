import os, sys
from environs import Env
from csci_utils.hashings import hash_helper
import json
import websocket_client
import random, time
import read_arduino



def iam_alive() -> str:
    """
    simple msg to test that the template
    can  be tested with pytest
    """
    # use of hashings
    print(f"hash(gorlins) = {hash_helper.get_user_id('gorlins')}")
    print(f"hash(artexmg) = {hash_helper.get_user_id('artexmg')}")

    return "IAMALIVE"

def routine():
    my_sensor = read_arduino.MegaSensor()
    my_sensor.log_serial(output_dir='sensor_data', file_name='deamon')

if __name__ == "__main__":
    # Idea taken from
    # https://betterprogramming.pub/how-to-make-sense-of-distributed-processing-with-python-daemons-586ee12f7f4d
    #
    print(f"Process parent PID{os.getpid()}")
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit()
    except OSError as error:
        print(f"Fork failed {error.errno} {e.strerror} {sys.stderr}")
        sys.exit(1)

    print("Fledging process")

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            print(f"Fledged deamon PID {pid}")
            sys.exit()
    except OSError as error:
        print(f"Fork 2 failed {error.errno} {e.strerror} {sys.stderr}")
        sys.exit(1)

    print("Executing routine in background.......")
    routine()
    # quick and dirty setup for using CSCI_UTILS

    # ws=websocket_client.WebSocket()
    #
    # ws.connect('ws://localhost:8000/ws/mega_sensor/')
    #
    # for i in range(1000):
    #     time.sleep(1)
    #     ws.send(json.dumps({'value':random.randint(1,100)}))

