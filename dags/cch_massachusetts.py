"""
Submit an AWS batch job for massachusetts
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.awsbatch_operator import AWSBatchOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 5, 3),
    "email": ["dingli@takemobi.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2020, 1, 1),
}

jobNamePrefix = 'cch_map_update_airflow_massachusetts_'
jobDefinition = 'arn:aws:batch:us-east-1:825437374987:job-definition/cch_map_update_job_definition:3'
jobQueue = 'arn:aws:batch:us-east-1:825437374987:job-queue/cch-map-update-job-queue'

containerOverrides={
    'memory': 8192,
    'environment': [
        {
            'name': 'CCH_AWS_S3_OBJECT_PREFIX',
            'value': 'maps/massachusetts-ch/'
        },
        {
            'name': 'MAP_URL',
            'value': 'https://download.geofabrik.de/north-america/us/massachusetts-latest.osm.pbf'
        },
        {
            'name': 'BATCH_AWS_ACCESS_KEY_ID',
            'value': 'AKIAINCVZSL7U3PVBHUA'
        },
        {
            'name': 'CCH_AWS_S3_BUCKET',
            'value': 'mobility-data-static'
        },
        {
            'name': 'MAP_NAME',
            'value': 'massachusetts-latest'
        },
        {
            'name': 'BATCH_AWS_SECRET_ACCESS_KEY',
            'value': 'DI9SPRWYLxNvhQJdISydNmD2xczoUIKp0olHYON6'
        },
    ],
}


dag = DAG("cch_massachusetts", default_args=default_args, catchup=False, schedule_interval="30 1 * * *",)

t1 = AWSBatchOperator(task_id="submit_cch",
                      job_name=(jobNamePrefix + datetime.now().strftime('%Y%m%d%H%M')),  
                      job_definition=jobDefinition,
                      job_queue=jobQueue,
                      overrides=containerOverrides,
                      aws_conn_id="aws_mobi",
                      region_name="us-east-1",
                      dag=dag);







