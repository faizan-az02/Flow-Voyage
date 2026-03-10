import sys
sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

from modules.ingestion import ingest_data
from modules.validation import validate_data
from modules.preprocessing import impute_age, impute_embarked
from modules.encoding import encode_features
from modules.training import train_model
from modules.evaluation import evaluate_model
from modules.branching import branch_on_accuracy
from modules.register import register_model
from modules.reject import reject_model


default_args = {
    "owner":"airflow",
    "start_date":datetime(2024,1,1),
    "retries":2
}


with DAG(
    dag_id="flowvoyage_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:


    start = EmptyOperator(task_id="start")

    ingest = PythonOperator(
        task_id="data_ingestion",
        python_callable=ingest_data
    )

    validate = PythonOperator(
        task_id="data_validation",
        python_callable=validate_data
    )

    age = PythonOperator(
        task_id="impute_age",
        python_callable=impute_age
    )

    embarked = PythonOperator(
        task_id="impute_embarked",
        python_callable=impute_embarked
    )

    encode = PythonOperator(
        task_id="encode_features",
        python_callable=encode_features
    )

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    evaluate = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model
    )

    branch = BranchPythonOperator(
        task_id="branch_on_accuracy",
        python_callable=branch_on_accuracy
    )

    register = PythonOperator(
        task_id="register_model",
        python_callable=register_model
    )

    reject = PythonOperator(
        task_id="reject_model",
        python_callable=reject_model
    )

    end = EmptyOperator(task_id="end")


    start >> ingest >> validate >> age >> embarked >> encode >> train >> evaluate >> branch
    branch >> register >> end
    branch >> reject >> end