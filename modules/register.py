import mlflow


def register_model():

    print("Registering model in MLflow registry")

    mlflow.register_model(
        "runs:/model",
        "TitanicSurvivalModel"
    )