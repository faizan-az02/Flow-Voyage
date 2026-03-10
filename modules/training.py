import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("http://mlflow:5000")


def train_model(**context):

    mlflow.set_experiment("flowvoyage_pipeline")

    df = pd.read_csv("/opt/airflow/data/encoded.csv")

    bool_cols = df.select_dtypes(include="bool").columns
    df[bool_cols] = df[bool_cols].astype(int)

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    C_value = 1.0

    model = LogisticRegression(
        C=C_value,
        max_iter=200
    )

    with mlflow.start_run() as run:

        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("C", C_value)
        mlflow.log_param("dataset_size", len(df))

        mlflow.log_metric("accuracy", accuracy)

        mlflow.sklearn.log_model(
            model,
            artifact_path="model"
        )

    ti = context["ti"]

    ti.xcom_push(
        key="X_test",
        value=X_test.to_json(orient="split")
    )

    ti.xcom_push(
        key="y_test",
        value=y_test.to_json(orient="split")
    )

    ti.xcom_push(
        key="run_id",
        value=run.info.run_id
    )