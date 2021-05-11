uploader package
================


Implemented as a deamon waiting for  data files to be written, to process and upload then to S3 to finally mark the folders as "touched".
This module has the option to be executed in the foreground, vs background, and still generating files

**DAG for processing and upload**: Reads from sensor data, process all batches and upload to S3 using DASK and Luigi


Implemented following **PEP 3143** standard daemon process lib

Submodules
----------

uploader.cli module
-------------------

.. automodule:: uploader.cli
   :members:
   :undoc-members:
   :show-inheritance:

uploader.up\_deamon module
--------------------------

.. automodule:: uploader.up_deamon
   :members:
   :undoc-members:
   :show-inheritance:

uploader.up\_tasks module
-------------------------

.. automodule:: uploader.up_tasks
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: uploader
   :members:
   :undoc-members:
   :show-inheritance:
