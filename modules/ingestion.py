from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 2
}


dag = DAG(
    dag_id="flowvoyage_mlops_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)