import os, time
import argparse
import logging
import daemon
from daemon import pidfile
from typing import Dict

import up_deamon

def set_logger(args: Dict)->logging.getLogger:
    """
    Setting logger with verbosity levels
    if args.verbosity = true then loging lever is set to debug

    Args:
        args (Dict): cli parameters

    Returns:
        logger (logger.getLogger): logger object
    """
    log_level = logging.INFO
    if args.verbosity: log_level = logging.DEBUG

    logger = logging.getLogger(__name__)

    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    logger.addHandler(ch)

    return logger

def launch_deamon(args: Dict)->None:
    """
    Launch uploader daemon.
    if arg = -f then it is launched as a foreground process

    Args:
        args (Dict): cli arguments
    """

    # if flag --foreground is set, then no deamon is triggered
    if args.foreground:
        up_deamon.worker(args=args)
        print('foreground')
    else:
        with daemon.DaemonContext(
            working_directory=args.context,
            umask=0o002,
            pidfile=pidfile.TimeoutPIDLockFile(args.pidfile),
        ):
            up_deamon.worker(args=args)

def get_args(args: Dict = None) -> type(argparse.ArgumentParser()):
    """
    Get cli arguments that will be used to run the Daemon

    Args:
        args (Dict): cli arguments

    Returns:
        argparse.ArgumentParser: Dict structure with cli args

    """
    # creates the log directory if doesn't exist
    local_path = os.path.abspath(".")

    daemon_path = os.path.join(local_path, os.environ['DAEMON_DIR'])
    data_path = os.path.join(local_path, os.environ['SENSOR_DATA'])
    log_path = os.path.join(daemon_path, os.environ["LOG_DIR"])

    default_pidfile = os.path.join(log_path, 'uploader_deamon.pid')
    default_logfile = os.path.join(log_path, 'uploader_deamon.log')

    os.makedirs(log_path, exist_ok=True)

    parser = argparse.ArgumentParser(description="Command description.")
    parser.add_argument("-f", "--foreground", action="store_true", help="no deamon mode")
    parser.add_argument("-v","--verbosity",action="store_true", help="verbosity level")
    parser.add_argument("-p","--pidfile",default=default_pidfile,help="daemon pidfile")
    parser.add_argument("-l","--logfile",default=default_logfile,help="daemon logfile")
    parser.add_argument("-c","--context",default=daemon_path,help="context directory for Daemon")
    parser.add_argument("-d","--data_path", default=data_path, help="path for sensor data")


    return parser.parse_args(args=args)

def main(args: Dict = None)-> None:
    """
    Main logic to start Uploader Daemon. Use --help to review cli options

    Args:
        args (Dict): cli arguments

    """
    args = get_args(args=args)

    logger = set_logger(args)

    logger.info('launching deamon')

    logger.info(args.logfile)
    logger.info(args.pidfile)
    logger.info(args.verbosity)

    launch_deamon(args)
