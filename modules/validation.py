import pandas as pd


def validate_data(**context):

    ti = context["ti"]

    data_path = ti.xcom_pull(key="dataset_path", task_ids="data_ingestion")

    df = pd.read_csv(data_path)

    age_missing = df["Age"].isnull().mean()
    embarked_missing = df["Embarked"].isnull().mean()

    print("Age missing %:", age_missing)
    print("Embarked missing %:", embarked_missing)

    if age_missing > 0.30:
        raise ValueError("Too many missing values in Age")