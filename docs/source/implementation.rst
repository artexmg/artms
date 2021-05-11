Tool implementation
====================
The project is organized in three main modules:

- Serial Reader
    reads the serial port to acquire sensor data. Also, is responsible to store the info in local files and send (if connection available) a streaming flow using websockets.
- Uploader Daemon
    orchestrator based on luigi/DASK to read the data from the local files and upload them into S3 Buckets
- Streaming and Visualization
    Django site implemented using Channels, receiving the data stream from the serial reader. Also, presents the data as a real time graph.


Serial Reader
#############

**The heart of the system**: uses PySerial library to read the serial port
to collect sensor data coming from the monitor,
then writes the data as csv files in batches (atomically!)
and stream to websocket.

**Atomically designed**: batches are written first in a temporary file,
once the size is reached then the files within the batch is confirmed.
Batch size is controlled by env variables


**cli enabled & logging**: Demo mode: doesn't store files locally
Local mode:  doesn't need to connect to django
Logging activated


**Warning**: if you don't clean up the files it can prevent your
local pc to run!

.. figure:: images/serial_reader.png

Uploader
############

**Implemented as a deamon**: Keeps lurking in the background waiting for  data files to be written, to process and upload then to S3 to finally mark the folders as "touched". Warning, Multithread is not parallel!

**DAG for processing and upload**: Reads from sensor data, process all batches and upload to S3 using DASK and Luigi

**FG mode**: Daemon includes option to be executed in the foreground, still generating files

Implemented following **PEP 3143** standard daemon process lib

.. figure:: images/daemon_context.png


Streaming
##########

Stream's data in real-time fashion using Web Sockets over Django channels
Channels were created to handle asynchronous communication protocol, implementing async/await coroutines.

By nature, http is not designed to make realtime connections. WebSockets are two ways communication channel


.. image:: images/vaweform.png