import pandas as pd


def impute_age(**context):

    ti = context["ti"]
    data_path = ti.xcom_pull(key="data_path", task_ids="data_ingestion")

    df = pd.read_csv(data_path)

    df["Age"].fillna(df["Age"].median(), inplace=True)

    df.to_csv("/opt/airflow/data/processed.csv", index=False)


def impute_embarked(**context):

    df = pd.read_csv("/opt/airflow/data/processed.csv")

    df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

    df.to_csv("/opt/airflow/data/processed.csv", index=False)