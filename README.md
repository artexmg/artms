Asynchronous Real-time Monitor System
======================================

An (in)complete solution for real-time data acquisition and monitoring.

------------
[![Documentation Status](https://readthedocs.org/projects/artms/badge/?version=latest)](https://artms.readthedocs.io/en/latest/?badge=latest)

Don't foreget to [read the docs](https://artms.readthedocs.io/en/latest/index.html)

If you want to get a better idea of what this system is capable to do, please, watch the [live demo video](https://www.youtube.com/watch?v=XweiEuXdC8U&list=LLjaSVA-XuwBzd-5brcOsdNQ)


----

Creating the environment:
-----------

After cloning this repository locally, you would need to do some basic installation. 

My prefered way to isolate it is using pipenv wrapped over conda. First create a new conda environment, switch into it and install pipenv within

    conda create -n artsm python=3.8

    conda activate artsm

    conda install pipenv

Then install your dependencies in this new virtual environment  

    pipenv install --dev

You will need to setup the environment variables to your system and you will be ready to start.


Quick start guide
-----------------
----------------

These are the basic commands to start working with the system

Serial Reader

    pipenv run python -m serial_reader --help

First time execute it with no verbosity to see temporary directory

    pipenv run python -m serial_reader -l

open temporal file directory and then final directory

    open INFO:serial_reader.read_arduino:temp directory: /var/folders/h5/jh7gfnvs3gb6j6dvltzq15dr0000gn/T/tmphcfp4j6m

you can verify how the files are moving around and then move to next module

This is good time to trigger the uploader daemon


First verify aws has no files
  
      aws s3 ls s3://My_Bucket/sensor_data/

Then run uploader module
  
      pipenv run python -m uploader --help

      pipenv run python -m uploader -v

Look for daemon PID file

    cat daemon_context/logs/uploader_deamon.pid

    ps processID

Look daemon log to see what tasks have been executed

    more -f daemon_context/logs/uploader_deamon.log

verify aws has files and kill deamon

    aws s3 ls s3://<My_bucket>/sensor_data/

    kill -9 processID

go to shell screen and stop serial reader. This is a good time 
to delete sensor datafiles

streaming and visualization
    
    
start django (websocket will be listening now)
    
    pipenv run python django_for_arduino/manage.py runserver*
    
start serial reader mode -d (no files, just streaming)
    
    pipenv run python -m serial_reader -d
    
verify streaminng!!
    
    pipenv run python -m websockets ws://localhost:8000/ws/mega_sensor/


