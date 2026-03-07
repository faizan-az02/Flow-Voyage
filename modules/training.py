import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("http://mlflow:5000")

def train_model(**context):

    
    mlflow.set_experiment("flowvoyage_titanic_pipeline")

    df = pd.read_csv("/opt/airflow/data/encoded.csv")

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    C_value = 1.0

    model = LogisticRegression(C=C_value, max_iter=200)

    mlflow.start_run()

    model.fit(X_train, y_train)

    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("C", C_value)
    mlflow.log_param("dataset_size", len(df))

    mlflow.sklearn.log_model(model, "model")

    mlflow.end_run()

    ti = context["ti"]

    ti.xcom_push(key="X_test", value=X_test.to_json())
    ti.xcom_push(key="y_test", value=y_test.to_json())