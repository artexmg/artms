Serial Reader
=================

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