def reject_model(**context):

    accuracy = context["ti"].xcom_pull(key="accuracy")

    print(f"Model rejected due to low accuracy: {accuracy}")