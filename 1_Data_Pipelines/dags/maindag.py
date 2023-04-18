"""
ETL Data Pipeline Assessment
Author: MohanKumar Kannan
Date: 18-Mar-2023
"""
from airflow import DAG
from datetime import datetime
import logging
from airflow.decorators import task
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from utils import extraction, transformation, load
import constants as c


def process(input_file):
    """
    Call Extraction, Transformation and Load Routine
    :param input_file:
    :return:
    """
    fs = FileSensor(task_id='wait_for_' + input_file.replace('.', '_'), filepath=input_file)
    df = extraction(filename=fs.filepath)
    fs >> df
    transform_df = transformation(data_frame=df)
    load(transformed_df=transform_df, file_name=input_file)


dag = DAG(
    dag_id='Daily_Applicant_Transaction',
    description='Validate daily successful applications',
    schedule_interval='0 1 * * *',
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

