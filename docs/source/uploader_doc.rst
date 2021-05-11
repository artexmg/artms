Uploader
============

**Implemented as a deamon**: Keeps lurking in the background waiting for  data files to be written, to process and upload then to S3 to finally mark the folders as "touched". Warning, Multithread is not parallel!

**DAG for processing and upload**: Reads from sensor data, process all batches and upload to S3 using DASK and Luigi

**FG mode**: Daemon includes option to be executed in the foreground, still generating files

Implemented following **PEP 3143** standard daemon process lib

.. figure:: images/daemon_context.png
