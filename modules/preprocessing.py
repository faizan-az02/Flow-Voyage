import pandas as pd


def impute_age(**context):

    ti = context["ti"]
    data_path = ti.xcom_pull(key="dataset_path", task_ids="data_ingestion")

    df = pd.read_csv(data_path)

    df["Age"].fillna(df["Age"].median(), inplace=True)

    ti.xcom_push(
        key="Age_imputed",
        value=df["Age"].to_json(orient="split"),
    )


def impute_embarked(**context):

    ti = context["ti"]
    data_path = ti.xcom_pull(key="dataset_path", task_ids="data_ingestion")

    df = pd.read_csv(data_path)

    df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

    ti.xcom_push(
        key="Embarked_imputed",
        value=df["Embarked"].to_json(orient="split"),
    )