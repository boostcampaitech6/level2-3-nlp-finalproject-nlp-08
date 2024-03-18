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
    api = HfApi()
    model_path = './artifacts/checkpoint-16'
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
                        --output_model_path=$AIRFLOW_HOME/artifacts'
    )

    test_qg_with_userfeedback = BashOperator(
        task_id='test_qg',
        bash_command='python $AIRFLOW_HOME/qgmodel/test_qg.py \
                        --output_metric_path=$AIRFLOW_HOME/artifacts/after_finetuning_test_result.json \
                        --output_path=$AIRFLOW_HOME/artifacts/after_finetuning_prediction_result.csv \
                        --test_dataset_name=$AIRFLOW_HOME/artifacts/userfeedback_test.csv \
                        --model_name=$AIRFLOW_HOME/artifacts/checkpoint-16'
    )

    upload_model_to_hf_task = PythonOperator(
        task_id="modify_data_false_task",
        python_callable=upload_model_to_hf,
    )

    train_qg_with_userfeedback >> test_qg_with_userfeedback
    test_qg_with_userfeedback >> upload_model_to_hf_task
