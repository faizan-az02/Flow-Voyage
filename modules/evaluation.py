import pandas as pd
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def evaluate_model(**context):

    ti = context["ti"]

    X_test = pd.read_json(ti.xcom_pull(key="X_test", task_ids="train_model"))
    y_test = pd.read_json(ti.xcom_pull(key="y_test", task_ids="train_model"))

    # For simplicity we retrain model on full data (common practice in pipelines)
    df = pd.read_csv("/opt/airflow/data/encoded.csv")

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)

    ti.xcom_push(key="accuracy", value=accuracy)