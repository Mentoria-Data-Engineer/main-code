from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook


def create_empty_file(ti):
    file_path = '/opt/airflow/data/meu-arquivo.txt'
    with open(file_path, 'w') as file:
        pass


def upload_to_s3(filename: str, key: str, bucket_name: str) -> None:
    hook = S3Hook('s3_conn')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)


with DAG(
    dag_id='s3_dag',
    schedule_interval='@daily',
    start_date=datetime(2023, 5, 16),
    catchup=False
) as dag:

    task_create_empty_file = PythonOperator(
        task_id='create_empty_file',
        python_callable=create_empty_file
    )
    
    # Upload the file
    task_upload_to_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
        op_kwargs={
            'filename': '/opt/airflow/data/meu-arquivo.csv',
            'key': 'teste-users-8.csv',
            'bucket_name': 'dados-api-airflow'
        }
    )
    
    task_create_empty_file >> task_upload_to_s3
