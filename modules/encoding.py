import pandas as pd


def encode_features(**context):

    ti = context["ti"]

    data_path = ti.xcom_pull(key="dataset_path", task_ids="data_ingestion")

    if data_path is None:
        raise ValueError("Missing dataset_path XCom from data_ingestion for this DAG run.")

    df = pd.read_csv(data_path)

    age_json = ti.xcom_pull(task_ids="impute_age", key="Age_imputed")
    embarked_json = ti.xcom_pull(task_ids="impute_embarked", key="Embarked_imputed")

    if age_json is None or embarked_json is None:
        raise ValueError("Missing imputed Age or Embarked data from preprocessing tasks.")

    df["Age"] = pd.read_json(age_json, orient="split", typ="series").squeeze()
    df["Embarked"] = pd.read_json(embarked_json, orient="split", typ="series").squeeze()

    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

    df = pd.get_dummies(df, columns=["Embarked"])

    df.drop(["Name", "Ticket", "Cabin", "PassengerId"], axis=1, errors="ignore", inplace=True)

    df.to_csv("/opt/airflow/data/encoded.csv", index=False)