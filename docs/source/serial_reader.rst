serial\_reader package
======================

- The heart of the system.

uses PySerial library to read the serial port
to collect sensor data coming from the monitor,
then writes the data as csv files in batches (atomically!)
and stream to websocket.

- cli enabled & logging

Demo mode: doesn't store files locally
Local mode:  doesn't need to connect to django
Logging activated

- Atomically designed

Batches are written first in a temporary file,
once the size is reached then the files within the batch is confirmed.
Batch size is controlled by env variables

Warning:
If you don't clean up the files it can prevent your
local pc to run!


Submodules
----------

serial\_reader.cli module
-------------------------

.. automodule:: serial_reader.cli
   :members:
   :undoc-members:
   :show-inheritance:

serial\_reader.read\_arduino module
-----------------------------------

.. automodule:: serial_reader.read_arduino
   :members:
   :undoc-members:
   :show-inheritance:


Module contents
---------------

.. automodule:: serial_reader
   :members:
   :undoc-members:
   :show-inheritance:
