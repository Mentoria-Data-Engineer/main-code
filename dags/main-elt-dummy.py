import requests
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook

base_url = "https://dummyapi.io/data/v1"
app_id = "63eecdb28d3fc51cbfc2d4ab"

headers = {'Content-Type': 'application/json', 'app-id': app_id}

default_args = {
    'start_date': datetime(year=2023, month=4, day=10)
}

def fetch_data(data, limit):
    url = f"{base_url}/{data}?limit={limit}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}"

def fetch_user_profile(user_id):
    url = f"{base_url}/user/{user_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}"

def save_profiles_to_csv(profiles, filename):
    df = pd.DataFrame(profiles)
    df.to_csv(filename, index=False)

def extract_user_data():
    user_previews = fetch_data('user', 50)['data']
    return user_previews

def transform_user_data(user_previews):
    full_user_profiles = []
    for user in user_previews:
        user_id = user['id']
        user_profile = fetch_user_profile(user_id)
        full_user_profiles.append(user_profile)
    return full_user_profiles

def save_data_to_csv(full_user_profiles, **kwargs):
    ti = kwargs['ti']
    current_date = ti.execution_date.strftime('%Y-%m-%d')
    filename = f'/home/nay/airflow-main/data/full_user_profiles_{current_date}.csv' 
    save_profiles_to_csv(full_user_profiles, filename)

def upload_to_s3(**kwargs) -> None:
    ti = kwargs['ti']
    current_date = ti.execution_date.strftime('%Y-%m-%d')
    filename = f"/home/nay/airflow-main/data/full_user_profiles_{current_date}.csv"
    key = f"full_user_profiles_{current_date}.csv"
    bucket_name = 'dados-api-airflow'
    hook = S3Hook(aws_conn_id='s3_conn')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)

with DAG(
    dag_id='dummy_api_etl',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:

    task_extract_user_data = PythonOperator(
        task_id='extract_user_data',
        python_callable=extract_user_data
    )

    task_transform_user_data = PythonOperator(
        task_id='transform_user_data',
        python_callable=transform_user_data,
        op_args=[task_extract_user_data.output]
    )

    task_save_data_to_csv = PythonOperator(
        task_id='save_data_to_csv',
        python_callable=save_data_to_csv,
        op_args=[task_transform_user_data.output]
    )

    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        provide_context=True
    )

    task_extract_user_data >> task_transform_user_data >> task_save_data_to_csv >> task_upload_to_s3