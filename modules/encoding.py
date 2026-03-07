import pandas as pd


def encode_features(**context):

    df = pd.read_csv("/opt/airflow/data/processed.csv")

    df["Sex"] = df["Sex"].map({"male":0, "female":1})

    df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)

    df.drop(["Name","Ticket","Cabin","PassengerId"], axis=1, inplace=True)

    df.to_csv("/opt/airflow/data/encoded.csv", index=False)