from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python import BranchPythonOperator, PythonOperator

default_args = {
    "owner": "boostcamp",
    "depends_on_past": True,
    "start_date": datetime(2024, 3, 12),
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}
    

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

    train_qg_with_userfeedback >> test_qg_with_userfeedback
    
