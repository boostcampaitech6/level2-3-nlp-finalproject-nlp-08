from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    "owner": "boostcamp",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 12),
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}

database_args = {
    "table_name": "userfeedbacks",
    "timestamp": "created_at",
}


def check_added_data_number(**kwargs):
    last_checked_time = Variable.get("last checked time")
    target_number = 3

    hook = PostgresHook(postgres_conn_id="my_postgres")
    conn = hook.get_conn()

    cursor = conn.cursor()
    query = f"SELECT COUNT (question) FROM {kwargs['table_name']} WHERE {kwargs['timestamp']} > %s"
    cursor.execute(query, (last_checked_time,))

    result = cursor.fetchone()
    count = result[0]
    print(f"데이터 개수: {count}, 날짜: {last_checked_time}")

    cursor.close()
    conn.close()

    return "get_new_data_task" if count >= target_number else "skip_task"

def get_new_data(**kwargs):
    last_checked_time = Variable.get("last checked time")

    hook = PostgresHook(postgres_conn_id="my_postgres")
    conn = hook.get_conn()

    cursor = conn.cursor()
    query = f"SELECT * FROM {kwargs['table_name']} WHERE {kwargs['timestamp']} > %s"
    cursor.execute(query, (last_checked_time,))

    new_data = cursor.fetchall()
    new_time_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Variable.set("last checked time", new_time_value)

    cursor.close()
    conn.close()

    print(f"data: {new_data}", f"updated date: {last_checked_time}")

with DAG(
    dag_id='get_new_data',
    default_args=default_args,
    schedule_interval=timedelta(hours=6),
    tags=["my_dags"],
    catchup=False,    
) as dag:
    
    check_data_task = BranchPythonOperator(
        task_id="check_added_data_number_task",
        python_callable=check_added_data_number,
        op_kwargs=database_args
    )

    get_new_data_task = PythonOperator(
        task_id="get_new_data_task",
        python_callable=get_new_data,
        op_kwargs=database_args
    )

    skip_task = DummyOperator(
        task_id="skip_task"
    )

    check_data_task >> [get_new_data_task, skip_task]