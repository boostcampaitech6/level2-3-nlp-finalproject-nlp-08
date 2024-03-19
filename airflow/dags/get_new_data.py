from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from openai import OpenAI
import pandas as pd

import numpy as np

PROJECT_ROOT = "/home/song/level2-3-nlp-finalproject-nlp-08/airflow/"
OUTPUT_PATH_TEST = os.path.join(PROJECT_ROOT, "artifacts", "user_feedback_test.csv")
OUTPUT_PATH_TRAIN = os.path.join(PROJECT_ROOT, "artifacts", "user_feedback_train.csv")
OUTPUT_PATH_VALID = os.path.join(PROJECT_ROOT, "artifacts", "user_feedback_valid.csv")

DATA_TRUE_PATH = os.path.join(PROJECT_ROOT, "artifacts", "data_true.csv")
DATA_FALSE_PATH = os.path.join(PROJECT_ROOT, "artifacts", "data_false.csv")

API_KEY = Variable.get("OPENAI API KEY")

CLIENT = OpenAI(api_key=API_KEY)

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

COLUMNS = ['id', 'question', 'answer', 'context', 'like', 'created_at']

def preprocess_and_save_data(data, path):
    df = pd.DataFrame(data, columns=COLUMNS)
    df.drop(["like", "created_at"], axis=1, inplace=True)
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

    return "get_and_save_new_data_task" if count >= target_number else "skip_task"

def get_and_save_new_data(**kwargs):
    last_checked_time = Variable.get("last checked time")

    print(f"date: {last_checked_time}")

    hook = PostgresHook(postgres_conn_id="my_postgres")
    conn = hook.get_conn()

    cursor = conn.cursor()

    query_true = f'SELECT * FROM {kwargs["table_name"]} WHERE {kwargs["timestamp"]} > %s AND "like" = TRUE'
    cursor.execute(query_true, (last_checked_time,))
    data_true = cursor.fetchall()

    query_false = f'SELECT * FROM {kwargs["table_name"]} WHERE {kwargs["timestamp"]} > %s AND "like" = FALSE'
    cursor.execute(query_false, (last_checked_time,))
    data_false = cursor.fetchall()

    new_time_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Variable.set("last checked time", new_time_value)

    cursor.close()
    conn.close()

    print(f"data_true: {data_true}")
    print(f"data_false: {data_false}")

    preprocess_and_save_data(data_true, DATA_TRUE_PATH)
    preprocess_and_save_data(data_false, DATA_FALSE_PATH)

def generate_question(context, answer):
    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "이 시스템은 제공된 본문을 기반으로 하여, 제시된 답변이 명확한 답이 될 수 있는 의문문 형식의 질문을 생성합니다. 본문에서 주요 정보를 추출하여, 이를 바탕으로 한 질문을 구성하되, 질문이 제시된 답변을 직접적으로 요구하도록 해주세요. 생성된 질문은 포멀하고 전문적인 언어를 사용해야 하며, 본문의 내용과 직접적으로 관련되어야 합니다. 질문은 정보를 명확하게 요구하는 형태의 의문문이며, 사용자가 이해하기 쉬워야 합니다."},
            {"role": "user", "content": f"본문:{context}, 답변: {answer}"}
        ]
    )

    question = completion.choices[0].message.content

    return question

def modify_data_false():
    df_false = pd.read_csv(DATA_FALSE_PATH)

    for idx, row in df_false.iterrows():
        question = generate_question(row["context"], row["answer"])
        df_false.loc[idx, "question"] = question.strip()

    df_true = pd.read_csv(DATA_TRUE_PATH)
    
    df = pd.concat([df_true, df_false])
    df = df.sample(frac=1)
    
    df_list = np.array_split(df, 3)
    print("train data")
    df_list[0].to_csv(OUTPUT_PATH_TRAIN, mode='w', index=True, header=True)
    print("test data")
    df_list[1].to_csv(OUTPUT_PATH_TEST, mode='w', index=True, header=True)
    print("valid data")
    df_list[2].to_csv(OUTPUT_PATH_VALID, mode='w', index=True, header=True)

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

    get_and_save_new_data_task = PythonOperator(
        task_id="get_and_save_new_data_task",
        python_callable=get_and_save_new_data,
        op_kwargs=database_args
    )

    skip_task = DummyOperator(
        task_id="skip_task"
    )

    modify_data_false_task = PythonOperator(
        task_id="modify_data_false_task",
        python_callable=modify_data_false,
    )

    check_data_task >> get_and_save_new_data_task >> modify_data_false_task
    check_data_task >> skip_task
