import os, sys, time
import serial, websocket
import csv, json
import logging
from datetime import datetime
import tempfile
import shutil
import matplotlib

from environs import Env
env = Env()
env.read_env()

# ToDo: use Django to setup all system variables
ROWS_PER_FILE = 400  # number of rows in each data file
BATCH_SIZE = 5  # number of files in one single batch

# Check serial port and Baudrate in Arduino IDE
_BAUDRATE = os.environ["BAUD_RATE"]
_SERIAL_PORT = os.environ["SERIAL_PORT"]
_WS_URL = os.environ["WEBSOCKET"]

_DELIMITER = ","

BATCH_TIME = datetime.now().strftime("%d%m%y-%H%M%S")

local_output_path = os.path.abspath(os.environ["SENSOR_DATA"])

class MegaSensor:
    """
    Provides serial reading services and real time data streaming
    using websockets (if available)
    """

    header = [
        "ID",
        "Timestamp",
        "Pressure2 (cmH2O)", #2
        "Pressure1 (cmH2O)", #3
        "Flow1 (lpm)",       #4
        "Temp (Celcius)",    #5
    ]

    def __init__(self, header=header, baudrate=_BAUDRATE, serial_port=_SERIAL_PORT):
        """
        initializes the serial port
        input:
                header: list with csv header
                baudrate:
                serial_port:
        output:
                serial connection object
        """
        matplotlib.use("tkAgg")

        self.header = header
        self.baudrate = baudrate
        self.serial_port = serial_port
        self.serial = serial.Serial(_SERIAL_PORT, baudrate=_BAUDRATE)
        self.serial.flushInput()
        self.ws = None

    def confirm_path(self, tmp_path, final_path):
        """
        move temporary path to its final name
        in an atomic write fashin
        input:
            tmp_path
            final_path
        """
        logger = logging.getLogger(__name__)
        try:
            shutil.move(tmp_path, final_path)
        except IOError as error:
            logger.error(f"Path {tmp_path} to {final_path} renamed error\n{error}")
            raise
        return 0

    def make_batch_dir(self, batch_path):
        """
        created the directory for current batch
        input:
            batch_path
        """
        logger = logging.getLogger(__name__)
        try:
            os.makedirs(batch_path, exist_ok=True)
        except IOError as error:
            logger.error(
                f"Batch directory {batch_path} were not created exception\n {error}"
            )
            raise
        return 0

    def get_websocket(self, url, host="localhost", port=8000):
        """
        connects to Websocket
        """
        logger = logging.getLogger(__name__)

        try:
            ws = websocket.WebSocket()
            ws.connect(f"ws://{host}:{port}/{url}")
        except:
            logger.info(f"WebSocket url:{url} host:{host} port:{port}")
            raise
        return ws

    def set_logger(self, args):
        logging.basicConfig()
        logging.getLogger(__name__).setLevel(logging.INFO)
        if args.verbosity:
            logging.getLogger(__name__).setLevel(logging.DEBUG)

        logger = logging.getLogger(__name__)
        return logger

    def log_serial(self, file_name, args):
        """
        reads serial port
        input:
            file_name:
            verbose:

        # ToDo: convert this to a Context Manager (if possible)
        """
        logger = self.set_logger(args)

        batch_id = 0
        ws = None
        if not args.local:
            ws = self.get_websocket(url=_WS_URL)

        # It writes to a temporary file until all files are generated
        with tempfile.TemporaryDirectory() as tmp:
            logger.info(f"temp directory: {tmp}")

            while True:
                try:
                    if args.demo_mode:
                        #only sends to websockets, no files are stored
                        self.websocket_loop(batch_id, ws, args)
                    else:
                        # writes data locally
                        # DANGER: could stop your local machine!
                        self.atomic_loop(tmp, file_name, batch_id, ws, args)

                    batch_id += 1
                except:
                    logger.error(f"Keyboard Interrupt {sys.exc_info()[0]}")
                    raise
                    # break

    def atomic_loop(self, tmp, file_name, batch_id, ws, args):
        """
        writes datafiles for a batch in a temporary directory,
        once the batch is finished, the whole directory is
        copied to final destination

        input:
            tmp: temporary directory
            file_name: base_name for each file within the directory
            batch_id: batch number, to be used to conform directory name
            ws: websocket connection (just a pass trhough)
            args: cli args
        """
        batch_name = f"batch-{BATCH_TIME}-{str(batch_id)}"
        batch_path = os.path.join(tmp, batch_name)

        self.make_batch_dir(batch_path)

        for file_id in range(BATCH_SIZE):

            file_format = f"{batch_name}-{file_name}-{str(file_id)}.csv"
            file_path = os.path.join(batch_path, file_format)

            row_offset = (
                batch_id + file_id
            ) * ROWS_PER_FILE + batch_id * ROWS_PER_FILE * (BATCH_SIZE - 1)

            # ToDo make this call async (coroutine)
            self.write_batch(file_path, row_offset, ws, args)

        # once the batch is finished it is moved to the permanent destination
        atomic_batch_path = os.path.join(local_output_path, batch_name)
        self.confirm_path(batch_path, atomic_batch_path)

    def websocket_loop(self, rownum, ws, args):
        """
        sends data to websocket
        NOTE: we need this function to calculate
              the right rownum if not called
              from file write loop
        """
        # ToDo make this call async (coroutine)

        dataline = self.read_data(rownum, ws, args)
        self.websocket_send(dataline, ws, args)

    def write_batch(self, file_path, row_offset, ws, args):
        """
        manages writing files in a batch fashion
        tries to send data to WebSocket (if open)
            cols: column header
            file_path: output_path
            row_offset: next batch row_id
            ws: websocket_client connection
            verbose: prints serial readings

        ToDo: convert this to a Context Manager (if possible)
        """
        logging.getLogger(__name__)

        with open(file_path, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)
            writer.writeheader()

        with open(file_path, "a") as csv_file:
            for row_id in range(ROWS_PER_FILE):

                # composing the output line
                rownum = row_offset + row_id            

                dataline = self.read_data(rownum, ws, args)

                self.websocket_send(dataline, ws, args)
                
                # writes to file every ROWS_PER_FILE rows
                writer = csv.writer(csv_file, delimiter=_DELIMITER)
                writer.writerow(dataline)

    def read_data(self, rownum, ws, args):
        """
        manages writing files in a batch fashion
        tries to send data to WebSocket (if open)
            cols: column header
            file_path: output_path
            row_offset: next batch row_id
            ws: websocket_client connection
            verbose: prints serial readings

        ToDo: convert this to a Context Manager (if possible)
        """
        logger = logging.getLogger(__name__)
        # reads arduino serial port and parses bytes
        serial_bytes = self.serial.readline()
        string_rn = serial_bytes.decode()
        string = string_rn.rstrip().split(_DELIMITER)[:4]

        dataline = [rownum, time.time()] + string

        # if verbose flag then prints to logger
        if args.verbosity:
            logger.debug(f"{dataline}")
        return dataline

    def websocket_send(self, dataline, ws, args):
        """
        sends data via websocket
        could be deactivated to run locally
        """

        if args.local: return 0 # No websocket connection

        value = [float(dataline[2]),float(dataline[4])]
        ws.send(json.dumps({"value": value}))