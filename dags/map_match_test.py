
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.awsbatch_operator import AWSBatchOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 8, 1),
    "email": ["yingxiang@takemobi.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

jobNamePrefix = 'map_match_test_'
jobDefinition = 'arn:aws:batch:us-east-1:825437374987:job-definition/map_matching_master_job:1'
jobQueue = 'arn:aws:batch:us-east-1:825437374987:job-queue/map-matching-master-job-queue'

containerOverrides={
    'memory': 2048,
    'environment': [
        {
            'name': 'BATCH_AWS_ACCESS_KEY_ID',
            'value': 'AKIAINCVZSL7U3PVBHUA'
        },
        {
            'name': 'BATCH_AWS_SECRET_ACCESS_KEY',
            'value': 'DI9SPRWYLxNvhQJdISydNmD2xczoUIKp0olHYON6'
        },
    ],
}


dag = DAG("map_matching_master", default_args=default_args, catchup=False, schedule_interval="0 * * * *",)

t1 = AWSBatchOperator(task_id="submit_map_matching",
                      job_name=(jobNamePrefix + datetime.now().strftime('%Y%m%d%H%M')),  
                      job_definition=jobDefinition,
                      job_queue=jobQueue,
                      overrides=containerOverrides,
                      aws_conn_id="aws_mobi",
                      region_name="us-east-1",
                      dag=dag);







