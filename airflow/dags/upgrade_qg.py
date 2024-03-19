from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import BranchPythonOperator, PythonOperator

from huggingface_hub import HfApi

default_args = {
    "owner": "boostcamp",
    "depends_on_past": True,
    "start_date": datetime(2024, 3, 12),
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}
    

def upload_model_to_hf():
    api = HfApi(
        endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
        token="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", # Token is not persisted on the machine.
    )
    model_path = './artifacts/model_saved'
    repo_id = '2024-level3-finalproject-nlp-8/qg_model_airflow' 

    api.upload_folder(
        folder_path=model_path,
        repo_id=repo_id,
        repo_type="model"
    )

with DAG(
        dag_id='train_test_qg',
        default_args=default_args,
        schedule_interval='@once',
        tags=['my_dags']
) as dag:
    train_qg_with_userfeedback = BashOperator(
        task_id="train_qg",
        bash_command='python $AIRFLOW_HOME/qgmodel/train_qg.py \
                        --train_dataset_name=$AIRFLOW_HOME/artifacts/userfeedback_train.csv \
                        --output_model_path=$AIRFLOW_HOME/artifacts \
                        --valid_dataset_name=$AIRFLOW_HOME/artifacts/userfeedback_valid.csv'

    )

    change_model_path = BashOperator(
        task_id="change_model_path",
        bash_command='mv $(find $AIRFLOW_HOME/artifacts -name \*checkpoint\* -type d -maxdepth 1 -print | head -n1) \
                        $AIRFLOW_HOME/artifacts/model_saved'
    )

    test_qg_with_userfeedback = BashOperator(
        task_id='test_qg',
        bash_command='python $AIRFLOW_HOME/qgmodel/test_qg.py \
                        --output_metric_path=$AIRFLOW_HOME/artifacts/after_finetuning_test_result.json \
                        --output_path=$AIRFLOW_HOME/artifacts/after_finetuning_prediction_result.csv \
                        --test_dataset_name=$AIRFLOW_HOME/artifacts/userfeedback_test.csv \
                        --model_name=$AIRFLOW_HOME/artifacts/model_saved'
    )

    upload_model_to_hf_task = PythonOperator(
        task_id="modify_data_false_task",
        python_callable=upload_model_to_hf,
    )

    train_qg_with_userfeedback >> change_model_path
    change_model_path >> test_qg_with_userfeedback
    test_qg_with_userfeedback >> upload_model_to_hf_task
