def branch_on_accuracy(**context):

    accuracy = context["ti"].xcom_pull(key="accuracy")

    if accuracy >= 0.80:
        return "register_model"
    else:
        return "reject_model"