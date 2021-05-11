Quick start guide
=================

These are the basic commands to start working with the system

1 Serial Reader
-----------------

# Serial Reader Console

    *pipenv run python -m serial_reader --help*

# no verbosity to see temp file

    *pipenv run python -m serial_reader -l*

# open temporal file directory
# open final directory

    *open INFO:serial_reader.read_arduino:temp directory: /var/folders/h5/jh7gfnvs3gb6j6dvltzq15dr0000gn/T/tmphcfp4j6m*

# you can see how the files are moving around and then move to next module

2 Uploader
--------------

# First verify aws has no files
    *aws s3 ls s3://My_Bucket/sensor_data/*

# Then run uploader module
    *pipenv run python -m uploader --help*

    *pipenv run python -m uploader -v*

# Look for daemon PID file

    *cat daemon_context/logs/uploader_deamon.pid*
    *ps processID*

# Look daemon log to see what tasks have been executed

    *more -f daemon_context/logs/uploader_deamon.log*

# verify aws has files and kill deamon

    *aws s3 ls s3://<My_bucket>/sensor_data/*

    *kill -9 processID*

# go to shell screen and stop serial reader
# delete sensor data files

3 streaming and visualization
-----------------------------

# a. start django (websocket will be listening now)
# Django console

    *pipenv run python django_for_arduino/manage.py runserver*

# b. start serial reader mode -d (no files, just streaming)
# serialReader console

    *pipenv run python -m serial_reader -d*

# c. verify streaminng!!
# independent console

    *pipenv run python -m websockets ws://localhost:8000/ws/mega_sensor/*

 # d. Look server!

    *localhost:8000*

 # to open to public you need to listen inbound/outbound

    *pipenv run django_for_arduino/manage.py runserver 0.0.0.0:8000*

# b. verify index.html has the right websocket IP

# c. restart SerialReader
    *pipenv run python -m                                                                                                                                                                            serial_reader -d*