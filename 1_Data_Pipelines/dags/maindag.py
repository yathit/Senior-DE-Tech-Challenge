"""
ETL Data Pipeline Assessment
Author:
Date: 18-Mar-2023
"""
from airflow import DAG
from datetime import datetime
import logging
from airflow.decorators import task
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from utils import extraction, transformation, load, delete_file
import constants as c


def process(file_name):
    """
    Call Extraction, Transformation and Load Routine
    :param file_name:
    :return:
    """
    input_file_path = "".join([c.input_path, file_name])

    fs = FileSensor(task_id='wait_for_file',
                    filepath=input_file_path,
                    poke_interval=2,
                    timeout=3 * 2
                    )
    df = extraction(filename=input_file_path)
    tf = transformation(data_frame=df)
    loader = load(transformed_df=tf, file_name=file_name)
    del_file = delete_file(input_file_path)

    fs >> df >> tf >> loader >> del_file


dag = DAG(
    dag_id='Hourly_Applicant_Transaction',
    description='Validate hourly successful applications',
    schedule_interval=None,  # '0 * * * *',
    start_date=datetime(2023, 4, 16),
    catchup=False
)

with dag:
    @task
    def begin_task():
        logging.info('Pipeline Started {}'.format(datetime.utcnow().isoformat()))


    @task
    def end_task():
        logging.info('Pipeline Ended SuccessFully {}'.format(datetime.utcnow().isoformat()))


    pipes = []
    for fn in c.input_file_names:
        with TaskGroup(fn.replace('.', '_')) as pipeline:
            process(fn)
            pipes.append(pipeline)

    begin_task() >> pipes >> end_task()
