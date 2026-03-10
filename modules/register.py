import mlflow
from mlflow.tracking import MlflowClient


def register_model():

    print("Registering model in MLflow registry")

    client = MlflowClient()

    experiment = client.get_experiment_by_name("flowvoyage_pipeline")

    if experiment is None:
        print("No experiment found for model registration.")
        return

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="params.model_type = 'LogisticRegression'",
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )

    if not runs:
        print("No runs found for model registration.")
        return

    run_id = runs[0].info.run_id
    model_uri = f"runs:/{run_id}/model"

    mlflow.register_model(
        model_uri,
        "TitanicSurvivalModel"
    )