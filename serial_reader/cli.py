import argparse
import logging
import os

# from read_arduino import MegaSensor
from serial_reader.read_arduino import MegaSensor


def set_logger(args):
    """
    Setting my logger and arguments
    """
    log_level = logging.INFO
    if args.verbosity:
        log_level = logging.DEBUG

    logger = logging.getLogger(__name__)

    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    logger.addHandler(ch)

    return logger

def main(args=None):
    """
    Manages how the serial deamon should be launch (if so!)
    """
    # created the log directory if doesn't exist
    local_path = os.path.abspath(".")
    log_path = os.path.join(local_path, os.environ["LOG_DIR"])
    
    logfile=os.path.join(log_path, "serial_reader_deamon.log")
    pidfile=os.path.join(log_path, "serial_reader_deamon.pid")

    os.makedirs(log_path, exist_ok=True)

    parser = argparse.ArgumentParser(description="Command description.")
    parser.add_argument("-v", "--verbosity", action="store_true", help="verbosity")
    parser.add_argument("-d", "--demo_mode", action="store_true", help="no data is stored")
    parser.add_argument("-l", "--local", action="store_true", help="local, no django no websockets needed!")
    
    args = parser.parse_args(args=args)
    set_logger(args)

    my_sensor = MegaSensor()

    my_sensor.log_serial("my_data", args)
