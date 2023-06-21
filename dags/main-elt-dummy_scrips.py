from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook
from scripts.extract_transform_load_dummy import fetch_data, fetch_user_profile, save_profiles_to_csv, extract_user_data, transform_user_data, save_data_to_csv, upload_to_s3

default_args = {
    'start_date': datetime(year=2023, month=3, day=20)
}


with DAG(
    dag_id='dummy_api_etl_scrips',
    default_args=default_args,
    schedule_interval='0 9 * * 1-5'
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