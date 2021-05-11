import os
import time
import logging
import luigi
from luigi import Task, Parameter, ExternalTask
from typing import Dict, Any

from csci_utils.luigi.task import TargetOutput, Requires, Requirement
from csci_utils.luigi.dask.target import ParquetTarget, CSVTarget
from csci_utils.hashings.hash_helper import get_user_id

from environs import Env
env = Env()
env.read_env()

hash_id = get_user_id(os.environ['HASH_ID'])
_S3_BUCKET = os.environ["S3_BUCKET"].format(hash_id=hash_id)

_INPUT_PATH=os.path.abspath(os.environ['SENSOR_DATA'])
_INPUT_PATH="./sensor_data"
input_path = os.path.abspath(os.environ['SENSOR_DATA'])



class SensorData(ExternalTask):
    """
    Reads csv files generated by Arduino Sensor

    Args:
        ExternalTask (luigi.Task): luigi task with origin data

    """
    file_pattern = "{task.input_path}"
    input_path=luigi.Parameter()

    output = TargetOutput(
        file_pattern=file_pattern,
        ext="",
        target_class=CSVTarget,
        glob="*.csv",
        flag=None,
    )

class UploadData(Task):
    """
    Derives PIP/PEEP/RR and upload sensor files to S3

    Args:
        Task(luigi.Task): LuigiTask class to upload into S3

    """
    input_path = luigi.Parameter()
    batch_id = luigi.Parameter(default="")
    file_pattern = _S3_BUCKET+"/{task.batch_id}"

    requires = Requires()
    sensor = Requirement(SensorData)
    output = TargetOutput(ext=".parquet",
                          target_class=ParquetTarget,
                          flag=None,
                          glob="",
                          file_pattern=file_pattern)

    def run(self):
        ddf = self.input()['sensor'].read_dask()
        self.output().write_dask(ddf,
                                 engine="fastparquet",
                                 compression="gzip",
                                 )

def push_files(input_path: str, batch_id: str, args: Dict) -> Any:
    """
    upload files to S3

    Args:
        input_path (str): source data path
        batch_id: str): number of batch
        args (Dict): cli arguments
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if args.verbosity:
        logger.setLevel(logging.INFO)

    # Important! detailed_summary=True
    # to get the type of status needed upstream!
    task_status = luigi.build([UploadData(input_path=input_path,
                            batch_id=batch_id)],
                            local_scheduler=True,
                            detailed_summary=True,
                         )

    return task_status


if __name__ == "__main__":
    batch_id = 'sensor_data-batch-3'
    local_path = os.path.abspath(os.environ['SENSOR_DATA'])
    input_path = os.path.join(local_path,batch_id)

    push_files(input_path=input_path,batch_id=batch_id)