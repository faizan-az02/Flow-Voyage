import pandas as pd

def ingest_data(**context):

    path = "/opt/airflow/data/titanic.csv"

    df = pd.read_csv(path)

    print("Dataset shape:", df.shape)
    print("Missing values:")
    print(df.isnull().sum())

    ti = context["ti"]
    ti.xcom_push(key="dataset_path", value=path)