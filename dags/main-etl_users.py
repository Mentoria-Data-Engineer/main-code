import json
import requests
import pandas as pd
import os
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.hooks.S3_hook import S3Hook


default_args = {
    'start_date': datetime(year=2023, month=4, day=10)
}


def extract_users(url: str, **kwargs) -> None:
    ti = kwargs['ti']
    res = requests.get(url)
    json_data = json.loads(res.content)
    ti.xcom_push(key='extracted_users', value=json_data)


def transform_users(**kwargs) -> None:
    ti = kwargs['ti']
    users = ti.xcom_pull(key='extracted_users', task_ids=['extract_users'])[0]
    transformed_users = []
    for user in users:
        transformed_users.append({
            'ID': user['id'],
            'Name': user['name'],
            'Username': user['username'],
            'Email': user['email'],
            'Address': f"{user['address']['street']}, {user['address']['suite']}, {user['address']['city']}",
            'PhoneNumber': user['phone'],
            'Company': user['company']['name']
        })
    ti.xcom_push(key='transformed_users', value=transformed_users)


def load_users(**kwargs) -> None:
    ti = kwargs['ti']
    current_date = ti.execution_date.strftime('%Y-%m-%d')
    transformed_users = ti.xcom_pull(key='transformed_users', task_ids=['transform_users'])[0]
    df = pd.DataFrame(transformed_users)
    filename = f"/home/nay/airflow-main/data/users_{current_date}.csv"
    df.to_csv(filename, index=False)


def upload_to_s3(**kwargs) -> None:
    ti = kwargs['ti']
    current_date = ti.execution_date.strftime('%Y-%m-%d')
    filename = f"/home/nay/airflow-main/data/users_{current_date}.csv"
    key = f"users_{current_date}.csv"
    bucket_name = 'dados-api-airflow'
    hook = S3Hook(aws_conn_id='s3_conn')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)


with DAG(
    dag_id='etl_users',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:

    task_extract_users = PythonOperator(
        task_id='extract_users',
        python_callable=extract_users,
        op_kwargs={'url': 'https://jsonplaceholder.typicode.com/users'},
        provide_context=True
    )

    task_transform_users = PythonOperator(
        task_id='transform_users',
        python_callable=transform_users,
        provide_context=True
    )

    task_load_users = PythonOperator(
        task_id='load_users',
        python_callable=load_users,
        provide_context=True
    )

    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        provide_context=True
    )

    task_extract_users >> task_transform_users >> task_load_users >> task_upload_to_s3
import json
import requests
import pandas as pd
import os
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.hooks.S3_hook import S3Hook


default_args = {
    'start_date': datetime(year=2023, month=4, day=10)
}


def extract_users(url: str, **kwargs) -> None:
    ti = kwargs['ti']
    res = requests.get(url)
    json_data = json.loads(res.content)
    ti.xcom_push(key='extracted_users', value=json_data)


def transform_users(**kwargs) -> None:
    ti = kwargs['ti']
    users = ti.xcom_pull(key='extracted_users', task_ids=['extract_users'])[0]
    transformed_users = []
    for user in users:
        transformed_users.append({
            'ID': user['id'],
            'Name': user['name'],
            'Username': user['username'],
            'Email': user['email'],
            'Address': f"{user['address']['street']}, {user['address']['suite']}, {user['address']['city']}",
            'PhoneNumber': user['phone'],
            'Company': user['company']['name']
        })
    ti.xcom_push(key='transformed_users', value=transformed_users)


def load_users(**kwargs) -> None:
    ti = kwargs['ti']
    current_date = ti.execution_date.strftime('%Y-%m-%d')
    transformed_users = ti.xcom_pull(key='transformed_users', task_ids=['transform_users'])[0]
    df = pd.DataFrame(transformed_users)
    filename = f"/home/nay/airflow-main/data/users_{current_date}.csv"
    df.to_csv(filename, index=False)


def upload_to_s3(**kwargs) -> None:
    ti = kwargs['ti']
    current_date = ti.execution_date.strftime('%Y-%m-%d')
    filename = f"/home/nay/airflow-main/data/users_{current_date}.csv"
    key = f"users_{current_date}.csv"
    bucket_name = 'dados-api-airflow'
    hook = S3Hook(aws_conn_id='s3_conn')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)


with DAG(
    dag_id='etl_users',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:

    task_extract_users = PythonOperator(
        task_id='extract_users',
        python_callable=extract_users,
        op_kwargs={'url': 'https://jsonplaceholder.typicode.com/users'},
        provide_context=True
    )

    task_transform_users = PythonOperator(
        task_id='transform_users',
        python_callable=transform_users,
        provide_context=True
    )

    task_load_users = PythonOperator(
        task_id='load_users',
        python_callable=load_users,
        provide_context=True
    )

    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        provide_context=True
    )

    task_extract_users >> task_transform_users >> task_load_users >> task_upload_to_s3
