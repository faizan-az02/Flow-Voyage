# FlowVoyage

FlowVoyage is an orchestrated machine learning pipeline that navigates
the journey from raw Titanic passenger data to survival prediction. The
system combines workflow orchestration with experiment tracking to
demonstrate a complete ML lifecycle including data ingestion,
validation, feature engineering, model training, evaluation, and
conditional model registration.

The pipeline is orchestrated using Apache Airflow while MLflow manages
experiment tracking, metrics logging, and model artifacts. All services
run inside Docker containers, creating a reproducible and scalable
environment for machine learning workflows.

------------------------------------------------------------------------

## Architecture

The system consists of the following core components:

-   **Apache Airflow** -- Orchestrates the end‑to‑end pipeline through
    DAG scheduling.
-   **MLflow Tracking Server** -- Stores experiments, metrics,
    parameters, and model artifacts.
-   **PostgreSQL** -- Airflow metadata database.
-   **Docker Compose** -- Containerized infrastructure for reproducible
    execution.

Pipeline execution is controlled by an Airflow DAG which triggers
sequential and parallel tasks across the ML workflow.

------------------------------------------------------------------------

## Pipeline Workflow

The FlowVoyage pipeline includes the following stages:

1.  **Data Ingestion**
    -   Loads the Titanic dataset.
    -   Logs dataset structure and missing values.
2.  **Data Validation**
    -   Checks missing value thresholds.
    -   Demonstrates retry behavior on validation failure.
3.  **Parallel Data Preprocessing**
    -   Missing value imputation for features such as `Age` and
        `Embarked`.
    -   Tasks run concurrently using Airflow parallel execution.
4.  **Feature Encoding**
    -   Encodes categorical variables.
    -   Removes irrelevant features.
5.  **Model Training**
    -   Trains a Logistic Regression classifier.
    -   Logs hyperparameters and dataset statistics to MLflow.
6.  **Model Evaluation**
    -   Computes Accuracy, Precision, Recall, and F1‑Score.
    -   Metrics are logged to MLflow for experiment comparison.
7.  **Branching Logic**
    -   Pipeline dynamically branches based on model performance.
    -   Models exceeding the accuracy threshold proceed to registration.
8.  **Model Registration**
    -   High performing models are registered in MLflow.
    -   Low performing models are rejected with logged reasons.

------------------------------------------------------------------------

## DAG Structure

The Airflow DAG coordinates the entire pipeline:

    start
      ↓
    data_ingestion
      ↓
    data_validation
      ↓
     ├── impute_age
     └── impute_embarked
            ↓
        encode_features
            ↓
          train_model
            ↓
         evaluate_model
            ↓
       branch_on_accuracy
          /        \
    register     reject
          \        /
              end

This design demonstrates:

-   Parallel task execution
-   Dependency‑driven orchestration
-   Dynamic branching
-   Reproducible ML experimentation

------------------------------------------------------------------------

## Repository Structure

    flow-voyage
    │
    ├── dags/
    │   └── flowvoyage_pipeline.py
    │
    ├── modules/
    │   ├── ingestion.py
    │   ├── validation.py
    │   ├── preprocessing.py
    │   ├── encoding.py
    │   ├── training.py
    │   ├── evaluation.py
    │   ├── branching.py
    │   ├── register.py
    │   └── reject.py
    │
    ├── data/
    │   └── titanic.csv
    │
    ├── mlruns/
    │
    ├── docker-compose.yaml
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## Running the System

Start the full stack:

    docker compose up --build

Airflow UI:

    http://localhost:8080

MLflow UI:

    http://localhost:5000

Once the services are running:

1.  Open Airflow UI
2.  Enable the `flowvoyage_pipeline` DAG
3.  Trigger pipeline execution

Each run logs experiments and metrics to MLflow for analysis.

------------------------------------------------------------------------

## Experiment Tracking

MLflow records:

-   Model hyperparameters
-   Dataset statistics
-   Evaluation metrics
-   Serialized model artifacts

Multiple pipeline runs allow comparison of model performance across
different hyperparameter configurations.

------------------------------------------------------------------------

## Technologies

-   Apache Airflow
-   MLflow
-   Scikit‑learn
-   Pandas
-   Docker
-   PostgreSQL

------------------------------------------------------------------------

