from datetime import datetime, timedelta
import pandas as pd

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from openai import OpenAI

OUTPUT_PATH = "../data/user_feedback.json"
DATA_FALSE_PATH = "../data/data_false.json"

CLIENT = OpenAI()

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

COLUMNS = ['id', 'context', 'answer', 'question', 'like', 'create_at']

def preprocess_and_save_data(data, path):
    df = pd.DataFrame(data, columns=COLUMNS)
    df.drop(["like", "created_at"], axis=1)
    df.to_csv(path, index=False)

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

    print(f"date: {last_checked_time}")

    hook = PostgresHook(postgres_conn_id="my_postgres")
    conn = hook.get_conn()

    cursor = conn.cursor()

    query_true = f"SELECT * FROM {kwargs['table_name']} WHERE {kwargs['timestamp']} > %s AND like = TRUE"
    cursor.execute(query_true, (last_checked_time,))
    data_true = cursor.fetchall()

    query_false = f"SELECT * FROM {kwargs['table_name']} WHERE {kwargs['timestamp']} > %s AND like = FALSE"
    cursor.execute(query_false, (last_checked_time,))
    data_false = cursor.fetchall()

    new_time_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Variable.set("last checked time", new_time_value)

    cursor.close()
    conn.close()

    print(f"data_true: {data_true}")
    print(f"data_false: {data_false}")

    preprocess_and_save_data(data_true, OUTPUT_PATH)
    preprocess_and_save_data(data_false, DATA_FALSE_PATH)

def generate_question(context, answer):
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "이 시스템은 제공된 본문을 기반으로 하여, 제시된 답변이 명확한 답이 될 수 있는 의문문 형식의 질문을 생성합니다. 본문에서 주요 정보를 추출하여, 이를 바탕으로 한 질문을 구성하되, 질문이 제시된 답변을 직접적으로 요구하도록 해주세요. 생성된 질문은 포멀하고 전문적인 언어를 사용해야 하며, 본문의 내용과 직접적으로 관련되어야 합니다. 질문은 정보를 명확하게 요구하는 형태이며, 사용자가 이해하기 쉬워야 합니다."},
            {"role": "user", "content": f"본문:{context}, 답변: {answer}"}
        ]
    )

    question = completion.choices[0].message.content

    return question

def save_data():
    pass

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

    check_data_task >> get_new_data_task 
    check_data_task >> skip_task