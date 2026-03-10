import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def evaluate_model(**context):

    ti = context["ti"]

    X_test_json = ti.xcom_pull(task_ids="train_model", key="X_test")
    y_test_json = ti.xcom_pull(task_ids="train_model", key="y_test")
    run_id = ti.xcom_pull(task_ids="train_model", key="run_id")

    if X_test_json is None or y_test_json is None:
        raise ValueError("Missing X_test or y_test XComs from train_model for this DAG run.")

    if run_id is None:
        raise ValueError("Missing run_id XCom from train_model for this DAG run.")

    X_test = pd.read_json(X_test_json, orient="split")
    y_test = pd.read_json(y_test_json, orient="split", typ="series").squeeze()

    model_uri = f"runs:/{run_id}/model"

    model = mlflow.sklearn.load_model(model_uri)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    with mlflow.start_run(run_id=run_id):

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

    ti.xcom_push(key="accuracy", value=accuracy)